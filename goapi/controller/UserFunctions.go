package controller

import (
	"errors"
	"os"
	"time"

	"github.com/foodshare/models"
	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt/v4"
	"github.com/joho/godotenv"
	"gorm.io/gorm"
)

func GenerateJWT(user *models.User) (string, error) {
	err := godotenv.Load(".env")
	if err != nil {
		return "", err
	}

	key := (os.Getenv("SECRET_KEY"))
	if key == "" {
		return "", errors.New("SECRET_KEY not found")
	}

	claims := jwt.MapClaims{
		"UserID": user.UserID,
		"Email":  user.Email,
		"exp":    time.Now().Add(time.Hour * 24).Unix(),
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString([]byte(key))
	if err != nil {
		return "", err
	}
	return tokenString, nil
}

func VerifyUser(db *gorm.DB) func(*fiber.Ctx) error {
	return func(c *fiber.Ctx) error {
		tokenString := c.Get("Authorization")
		if tokenString == "" {
			return c.Status(401).JSON(fiber.Map{
				"message": "No token found",
			})
		}

		tokenString = tokenString[7:]

		token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, errors.New("invalid token Here")
			}
			return []byte(os.Getenv("SECRET_KEY")), nil
		})

		if err != nil || !token.Valid {
			return c.Status(402).JSON(fiber.Map{
				"message": "Invalid token",
				"error":   err.Error(),
			})
		}

		claims, _ := token.Claims.(jwt.MapClaims)
		UserID := claims["UserID"]
		if UserID == nil {
			return c.Status(403).JSON(fiber.Map{
				"message": "User Id not found in tokens",
				"calims":  claims,
			})
		}

		return c.Status(200).JSON(fiber.Map{
			"message": "User verified",
			"id":      UserID,
		})

	}
}

