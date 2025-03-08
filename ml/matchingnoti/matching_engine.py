# matching_engine.py
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Organization, Donation, Claim, Notification, FoodCategoryPreference
from sklearn.preprocessing import MinMaxScaler
from geopy.distance import geodesic

class MatchingEngine:
    def __init__(self, db_session):
        self.db = db_session
        self.scaler = MinMaxScaler()
    
    def get_geocoordinates(self, address, city, state, zip_code):
        """
        Convert address to geocoordinates.
        In a production environment, this would use a geocoding service.
        For demonstration, we'll use dummy coordinates.
        """
        # Placeholder for geocoding logic
        # In production, use Google Maps API, Mapbox, or similar
        return (37.7749, -122.4194)  # Example coordinates (San Francisco)
    
    def calculate_perishability_score(self, donation):
        """
        Calculate how perishable a food donation is.
        Higher score = more perishable = higher priority
        """
        if not donation.is_perishable:
            return 0.2  # Non-perishable items get low priority
        
        # Calculate days until expiration
        if donation.expiration_date:
            days_until_expiration = (donation.expiration_date - datetime.utcnow()).days
            if days_until_expiration <= 0:
                return 0.0  # Expired items get zero score
            elif days_until_expiration <= 1:
                return 1.0  # Items expiring within 24 hours get highest priority
            elif days_until_expiration <= 3:
                return 0.8  # Items expiring within 3 days get high priority
            elif days_until_expiration <= 7:
                return 0.6  # Items expiring within a week get medium priority
            else:
                return 0.4  # Items with longer shelf life get lower priority
        
        # If no expiration date but marked perishable
        return 0.7  # Assume relatively high perishability
    
    def calculate_category_match_score(self, donation, organization):
        """
        Calculate how well the donation's food category matches the organization's preferences
        """
        # Get organization's food category preferences
        preferences = self.db.query(FoodCategoryPreference).filter_by(
            organization_id=organization.id
        ).all()
        
        preference_dict = {p.category: p.preference_level for p in preferences}
        
        # If the organization has a preference for this category
        if donation.category in preference_dict:
            # Scale from 0-10 to 0-1
            return preference_dict[donation.category] / 10.0
        
        # If the organization accepts all food types
        if len(preferences) == 0:
            return 0.5  # Neutral score
        
        # If the organization doesn't accept this food type
        return 0.1  # Low score but not zero to allow for some flexibility
    
    def calculate_distance_score(self, donation_org, recipient_org):
        """
        Calculate proximity score between donor and recipient
        Returns a score where 1.0 = very close, 0.0 = too far
        """
        # Get geocoordinates
        donor_coords = self.get_geocoordinates(
            donation_org.address, 
            donation_org.city, 
            donation_org.state, 
            donation_org.zip_code
        )
        
        recipient_coords = self.get_geocoordinates(
            recipient_org.address,
            recipient_org.city,
            recipient_org.state,
            recipient_org.zip_code
        )
        
        # Calculate distance in kilometers
        distance = geodesic(donor_coords, recipient_coords).kilometers
        
        # Check if within max pickup distance
        if distance > recipient_org.max_pickup_distance_km:
            return 0.0  # Too far
        
        # Normalize distance score (closer = higher score)
        return 1.0 - (distance / recipient_org.max_pickup_distance_km)
    
    def calculate_storage_compatibility_score(self, donation, organization):
        """
        Determine if the organization has appropriate storage for the donation
        """
        storage_req = donation.storage_requirements.lower() if donation.storage_requirements else "room_temperature"
        
        if storage_req == "frozen" and not organization.has_freezer:
            return 0.0  # Organization can't store frozen items
        
        if storage_req == "refrigerated" and not organization.has_refrigeration:
            return 0.0  # Organization can't store refrigerated items
        
        if storage_req == "dry" and not organization.has_dry_storage:
            return 0.3  # Organization lacks proper dry storage
            
        # Organization has appropriate storage
        return 1.0
    
    def calculate_allergen_compatibility_score(self, donation, organization):
        """
        Check if the donation contains allergens that the organization restricts
        """
        # Get organization's allergen restrictions
        org_restrictions = {r.allergen for r in organization.allergen_restrictions}
        
        # Get donation's allergens
        donation_allergens = {a.allergen for a in donation.allergens}
        
        # Check for conflicts
        conflicts = org_restrictions.intersection(donation_allergens)
        
        if conflicts:
            return 0.0  # Contains restricted allergens
        
        return 1.0  # No allergen conflicts
    
    def calculate_historical_acceptance_score(self, organization):
        """
        Calculate a score based on organization's history of accepting similar donations
        """
        # A real implementation would use ML to analyze past acceptance patterns
        # For this demo, we'll use the organization's acceptance rate
        
        if organization.acceptance_rate is None:
            return 0.5  # Neutral score for new organizations
        
        return min(1.0, organization.acceptance_rate)
    
    def calculate_capacity_score(self, donation, organization):
        """
        Determine if the organization has capacity for this donation
        """
        # In a real system, this would track current inventory levels
        # For demo purposes, use a simplified approach
        
        if organization.storage_capacity_kg is None:
            return 0.5  # Unknown capacity
        
        # Estimate donation weight in kg
        estimated_weight = donation.quantity if donation.unit == 'kg' else donation.quantity * 0.5
        
        # Calculate percent of organization's capacity this would use
        capacity_percentage = min(1.0, estimated_weight / organization.storage_capacity_kg)
        
        # Higher score for lower percentage (more available capacity)
        return 1.0 - capacity_percentage
    
    def find_matches_for_donation(self, donation_id, limit=10):
        """
        Find the best recipient matches for a given donation
        """
        # Get the donation
        donation = self.db.query(Donation).filter_by(id=donation_id).first()
        if not donation:
            return []
            
        # Get the donor organization
        donor_org = donation.donor_organization
        
        # Get all potential recipient organizations
        potential_recipients = self.db.query(Organization).filter(
            Organization.id != donor_org.id,  # Exclude the donor
            Organization.org_type != 'donor'  # Only include recipient organizations
        ).all()
        
        # Calculate match scores
        matches = []
        for org in potential_recipients:
            # Skip if organization restricts this food category entirely
            category_score = self.calculate_category_match_score(donation, org)
            if category_score == 0:
                continue
            
            # Skip if storage is incompatible
            storage_score = self.calculate_storage_compatibility_score(donation, org)
            if storage_score == 0:
                continue
            
            # Skip if allergens are incompatible
            allergen_score = self.calculate_allergen_compatibility_score(donation, org)
            if allergen_score == 0:
                continue
            
            # Calculate distance score
            distance_score = self.calculate_distance_score(donor_org, org)
            if distance_score == 0:
                continue  # Too far away
            
            # Calculate other scores
            perishability_score = self.calculate_perishability_score(donation)
            historical_score = self.calculate_historical_acceptance_score(org)
            capacity_score = self.calculate_capacity_score(donation, org)
            
            # Calculate overall match score (weighted average)
            overall_score = (
                perishability_score * 0.15 +
                category_score * 0.20 +
                distance_score * 0.25 +
                storage_score * 0.10 +
                allergen_score * 0.05 +
                historical_score * 0.15 +
                capacity_score * 0.10
            )
            
            matches.append({
                'organization_id': org.id,
                'organization_name': org.name,
                'match_score': overall_score,
                'distance_score': distance_score,
                'category_score': category_score,
                'storage_score': storage_score,
                'allergen_score': allergen_score,
                'historical_score': historical_score,
                'capacity_score': capacity_score
            })
        
        # Sort by match score (descending)
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Return top matches
        return matches[:limit]
    
    def find_matches_for_organization(self, organization_id, limit=10):
        """
        Find the best donation matches for a given organization
        """
        # Get the organization
        organization = self.db.query(Organization).filter_by(id=organization_id).first()
        if not organization:
            return []
        
        # Get all available donations
        available_donations = self.db.query(Donation).filter_by(
            status='available'
        ).filter(
            Donation.available_until > datetime.utcnow()
        ).all()
        
        # Calculate match scores
        matches = []
        for donation in available_donations:
            # Skip if donation comes from this organization
            if donation.donor_organization_id == organization_id:
                continue
                
            # Get donor organization
            donor_org = donation.donor_organization
            
            # Skip if storage is incompatible
            storage_score = self.calculate_storage_compatibility_score(donation, organization)
            if storage_score == 0:
                continue
            
            # Skip if allergens are incompatible
            allergen_score = self.calculate_allergen_compatibility_score(donation, organization)
            if allergen_score == 0:
                continue
            
            # Calculate distance score
            distance_score = self.calculate_distance_score(donor_org, organization)
            if distance_score == 0:
                continue  # Too far away
            
            # Calculate other scores
            category_score = self.calculate_category_match_score(donation, organization)
            perishability_score = self.calculate_perishability_score(donation)
            historical_score = self.calculate_historical_acceptance_score(organization)
            capacity_score = self.calculate_capacity_score(donation, organization)
            
            # Calculate overall match score (weighted average)
            overall_score = (
                perishability_score * 0.15 +
                category_score * 0.20 +
                distance_score * 0.25 +
                storage_score * 0.10 +
                allergen_score * 0.05 +
                historical_score * 0.15 +
                capacity_score * 0.10
            )
            
            matches.append({
                'donation_id': donation.id,
                'donation_title': donation.title,
                'donation_category': donation.category,
                'match_score': overall_score,
                'distance_score': distance_score,
                'category_score': category_score,
                'storage_score': storage_score,
                'expiration_date': donation.expiration_date,
                'donor_organization': donor_org.name
            })
        
        # Sort by match score (descending)
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Return top matches
        return matches[:limit]
    
    def create_notifications_for_donation(self, donation_id, match_threshold=0.6):
        """
        Generate notifications for the best matches for a donation
        """
        # Find matches
        matches = self.find_matches_for_donation(donation_id)
        
        # Get the donation
        donation = self.db.query(Donation).filter_by(id=donation_id).first()
        
        # Generate notifications for good matches
        notifications = []
        for match in matches:
            if match['match_score'] >= match_threshold:
                # Create notification object
                notification = Notification(
                    organization_id=match['organization_id'],
                    donation_id=donation_id,
                    message=f"New food donation available: {donation.title} ({donation.quantity} {donation.unit})",
                    notification_type="match",
                    relevance_score=match['match_score']
                )
                
                self.db.add(notification)
                notifications.append(notification)
        
        # Commit to database
        self.db.commit()
        
        return notifications
    
    def update_matching_model(self):
        """
        Update the matching model based on recent acceptance/rejection patterns
        In a real system, this would use more sophisticated ML techniques
        """
        # Get recent claims (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_claims = self.db.query(Claim).filter(
            Claim.claimed_at >= thirty_days_ago
        ).all()
        
        # Update organization acceptance rates
        org_claims = {}
        org_accepts = {}
        
        for claim in recent_claims:
            org_id = claim.recipient_organization_id
            
            if org_id not in org_claims:
                org_claims[org_id] = 0
                org_accepts[org_id] = 0
            
            org_claims[org_id] += 1
            
            if claim.status in ['accepted', 'completed']:
                org_accepts[org_id] += 1
        
        # Update organizations
        for org_id, claim_count in org_claims.items():
            if claim_count > 0:
                acceptance_rate = org_accepts[org_id] / claim_count
                
                org = self.db.query(Organization).filter_by(id=org_id).first()
                if org:
                    org.acceptance_rate = acceptance_rate
        
        self.db.commit()
        
        return {
            "organizations_updated": len(org_claims),
            "total_claims_analyzed": len(recent_claims)
        }
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class NotificationEngine:
    def __init__(self, db_session):
        self.db = db_session
        self.food_embeddings = self.load_food_embeddings()
        
    def load_food_embeddings(self):
        # Load precomputed food item embeddings from your AI model
        return np.load('food_embeddings.npy')
    
    def calculate_preference_score(self, user, donation):
        """Calculate personalized match score using AI"""
        # 1. Content-based filtering
        donation_embedding = self.food_embeddings[donation.category]
        user_profile = self.get_user_embedding(user)
        content_score = cosine_similarity([user_profile], [donation_embedding])[0][0]
        
        # 2. Collaborative filtering factors
        past_acceptance_rate = self.calculate_acceptance_rate(user)
        
        # 3. Contextual factors
        time_score = self.calculate_time_score(donation)
        
        # Combine scores
        total_score = (
            0.6 * content_score +
            0.3 * past_acceptance_rate +
            0.1 * time_score
        )
        
        return total_score
    
    def get_user_embedding(self, user):
        """Generate user embedding from preferences"""
        # Convert preferences to numerical representation
        cuisine_vec = self.encode_features(user.preferred_cuisines)
        diet_vec = self.encode_features(user.dietary_restrictions)
        return np.concatenate([cuisine_vec, diet_vec])
    
    def generate_notifications(self):
        """Main notification generation workflow"""
        # Get active users
        active_users = self.db.query(User).filter(
            User.last_active > datetime.utcnow() - timedelta(days=7)
        ).all()
        
        donations = self.db.query(Donation).filter(
            Donation.status == 'available'
        ).all()
        
        for user in active_users:
            user_prefs = self.db.query(UserPreferences).filter_by(user_id=user.id).first()
            if not user_prefs:
                continue
                
            for donation in donations:
                score = self.calculate_preference_score(user_prefs, donation)
                
                if score > 0.7:  # Threshold
                    self.create_notification(
                        user.id,
                        donation.id,
                        f"New {donation.category} matches your preferences!",
                        score
                    )
        
        self.create_expiration_reminders()
        self.create_system_alerts()
    
    def create_expiration_reminders(self):
        """Non-personalized expiration alerts"""
        expiring_soon = self.db.query(Donation).filter(
            Donation.expiration_date < datetime.utcnow() + timedelta(hours=24)
        ).all()
        
        for donation in expiring_soon:
            users = self.get_nearby_users(donation.location)
            for user in users:
                self.create_notification(
                    user.id,
                    donation.id,
                    f"Urgent: {donation.title} expiring soon!",
                    0.9  # High priority
                )
    
    def create_system_alerts(self):
        """General system notifications"""
        # Example: New features, maintenance alerts
        pass