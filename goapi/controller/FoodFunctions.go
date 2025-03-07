package controller

import (
	"strings"

	"github.com/foodshare/models"
	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func CreateFood(db *gorm.DB) func(*fiber.Ctx) error {
	return func(c *fiber.Ctx) error {
		food := new(models.Food)

		err := c.BodyParser(food)
		if err != nil {
			return c.Status(400).JSON(fiber.Map{
				"message": "Could not parse Body",
				"error":   err.Error(),
			})
		}

		err = db.Create(food).Error
		if err != nil {

			return c.Status(501).JSON(fiber.Map{
				"message": "Could not create food",
				"error":   err.Error(),
			})
		}

		return c.Status(201).JSON(fiber.Map{
			"message": "Recipe created",
			"data":    food,
		})
	}
}

func GetFood(db *gorm.DB) func(*fiber.Ctx) error {
	return func(c *fiber.Ctx) error {
		id := c.Params("id")

		food := new(models.Food)
		err := db.Where("ingredient_id = ?", id).First(food).Error
		if err != nil {
			if strings.Contains(err.Error(), "record not found") {
				return c.Status(404).JSON(fiber.Map{
					"message": "Food not found",
				})
			}

			return c.Status(500).JSON(fiber.Map{
				"message": "Could not retrieve Food",
				"error":   err.Error(),
			})
		}

		return c.Status(200).JSON(fiber.Map{
			"message": "Retrieved Food",
			"data":    food,
		})
	}
}

func GetFoods(db *gorm.DB) fiber.Handler {
	return func(c *fiber.Ctx) error {
		foods := new([]models.Food)

		err := db.Find(foods).Error
		if err != nil {
			return c.Status(500).JSON(fiber.Map{
				"message": "Could not retrieve foods",
				"error":   err.Error(),
			})
		}

		return c.Status(200).JSON(fiber.Map{
			"data": foods,
		})
	}
}