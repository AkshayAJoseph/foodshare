package models

import (
	"gorm.io/gorm"
)

type Food struct {
	FoodID   uint    `gorm:"primaryKey;autoIncrement" json:"id"`
	Name     *string `gorm:"type:varchar(255)" json:"name"`
	Lifespan int     `gorm:"type:int" json:"lifespan"`
	Quantity int     `gorm:"type:int" json:"quantity"`
}

func MigrateFood(db *gorm.DB) error {
	err := db.AutoMigrate(&Food{})
	return err
}
