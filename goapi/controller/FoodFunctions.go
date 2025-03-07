package controller

import (
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
