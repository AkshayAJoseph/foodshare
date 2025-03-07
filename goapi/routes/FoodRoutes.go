package routes

import (
	"github.com/foodshare/controller"
	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func FoodRoutes(db *gorm.DB, app *fiber.App) {
	api := app.Group("/api/v1")
	api.Post("/food", controller.CreateFood(db))
	api.Get("/food/:id", controller.GetFood(db))
	api.Get("/foods", controller.GetFoods(db))
}
