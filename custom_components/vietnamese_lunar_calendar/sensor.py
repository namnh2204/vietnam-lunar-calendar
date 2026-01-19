"""Sensor platform for Vietnamese Lunar Calendar."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_change

from .lunar_solar import (
    solar_to_lunar,
    lunar_to_solar,
    zodiac_year,
    zodiac_day,
    zodiac_month,
    day_in_week,
)

_LOGGER = logging.getLogger(__name__)

DOMAIN = "vietnamese_lunar_calendar"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Vietnamese Lunar Calendar sensors."""
    sensors = [
        LunarDateSensor(hass),
        LunarDaySensor(hass),
        LunarMonthSensor(hass),
        LunarYearSensor(hass),
        LunarFirstOrFifteenthSensor(hass),
        NextLunarFirstSensor(hass),
        NextLunarFifteenthSensor(hass),
    ]
    async_add_entities(sensors, True)


class LunarBaseSensor(SensorEntity):
    """Base class for lunar calendar sensors."""

    _attr_has_entity_name = True

    def __init__(self, hass: HomeAssistant, name: str, unique_id: str) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{unique_id}"
        self._attr_icon = "mdi:calendar-star"

    async def async_added_to_hass(self) -> None:
        """Set up a timer to update at midnight."""
        async_track_time_change(
            self.hass,
            self._async_update_at_midnight,
            hour=0,
            minute=0,
            second=0,
        )

    async def _async_update_at_midnight(self, now=None) -> None:
        """Update at midnight."""
        self.async_schedule_update_ha_state(True)


class LunarDateSensor(LunarBaseSensor):
    """Sensor for the full lunar date string."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        super().__init__(hass, "Ngày Âm Lịch", "lunar_date")
        self._attr_icon = "mdi:calendar-month"

    async def async_update(self) -> None:
        """Update the sensor."""
        now = datetime.now()
        lunar = solar_to_lunar(now.day, now.month, now.year)
        lunar_day, lunar_month, lunar_year, is_leap = lunar
        
        leap_str = " (nhuận)" if is_leap else ""
        zodiac = zodiac_year(lunar_year)
        
        self._attr_native_value = f"{lunar_day}/{lunar_month}{leap_str} năm {zodiac}"
        self._attr_extra_state_attributes = {
            "lunar_day": lunar_day,
            "lunar_month": lunar_month,
            "lunar_year": lunar_year,
            "is_leap_month": is_leap == 1,
            "zodiac_year": zodiac,
            "zodiac_day": zodiac_day(now.day, now.month, now.year),
            "zodiac_month": zodiac_month(lunar_month, lunar_year),
            "day_of_week": day_in_week(now.day, now.month, now.year),
            "solar_date": now.strftime("%d/%m/%Y"),
        }


class LunarDaySensor(LunarBaseSensor):
    """Sensor for the lunar day."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        super().__init__(hass, "Ngày Âm", "lunar_day")
        self._attr_icon = "mdi:calendar-today"

    async def async_update(self) -> None:
        """Update the sensor."""
        now = datetime.now()
        lunar = solar_to_lunar(now.day, now.month, now.year)
        self._attr_native_value = lunar[0]


class LunarMonthSensor(LunarBaseSensor):
    """Sensor for the lunar month."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        super().__init__(hass, "Tháng Âm", "lunar_month")
        self._attr_icon = "mdi:calendar-range"

    async def async_update(self) -> None:
        """Update the sensor."""
        now = datetime.now()
        lunar = solar_to_lunar(now.day, now.month, now.year)
        self._attr_native_value = lunar[1]
        self._attr_extra_state_attributes = {
            "is_leap_month": lunar[3] == 1,
        }


class LunarYearSensor(LunarBaseSensor):
    """Sensor for the lunar year."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        super().__init__(hass, "Năm Âm", "lunar_year")
        self._attr_icon = "mdi:calendar-star"

    async def async_update(self) -> None:
        """Update the sensor."""
        now = datetime.now()
        lunar = solar_to_lunar(now.day, now.month, now.year)
        self._attr_native_value = lunar[2]
        self._attr_extra_state_attributes = {
            "zodiac_year": zodiac_year(lunar[2]),
        }


class LunarFirstOrFifteenthSensor(LunarBaseSensor):
    """Sensor that is 'on' when it's the 1st or 15th of the lunar month."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        super().__init__(hass, "Mùng 1 hoặc Rằm", "is_first_or_fifteenth")
        self._attr_icon = "mdi:moon-full"

    async def async_update(self) -> None:
        """Update the sensor."""
        now = datetime.now()
        lunar = solar_to_lunar(now.day, now.month, now.year)
        lunar_day = lunar[0]
        
        if lunar_day == 1:
            self._attr_native_value = "Mùng 1"
        elif lunar_day == 15:
            self._attr_native_value = "Rằm"
        else:
            self._attr_native_value = "Không"
        
        self._attr_extra_state_attributes = {
            "is_first": lunar_day == 1,
            "is_fifteenth": lunar_day == 15,
            "lunar_day": lunar_day,
        }


class NextLunarFirstSensor(LunarBaseSensor):
    """Sensor for the next 1st of the lunar month (solar date)."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        super().__init__(hass, "Mùng 1 kế tiếp", "next_lunar_first")
        self._attr_icon = "mdi:moon-new"
        self._attr_device_class = SensorDeviceClass.DATE

    async def async_update(self) -> None:
        """Update the sensor."""
        now = datetime.now()
        lunar = solar_to_lunar(now.day, now.month, now.year)
        lunar_day, lunar_month, lunar_year, is_leap = lunar
        
        # Calculate next 1st day
        if lunar_day >= 1:
            # Move to next month's 1st
            next_month = lunar_month + 1
            next_year = lunar_year
            if next_month > 12:
                next_month = 1
                next_year += 1
        
        # Convert back to solar
        solar_date = lunar_to_solar(1, next_month, next_year, 0)
        if solar_date[0] != 0:
            next_first = datetime(solar_date[2], solar_date[1], solar_date[0])
            self._attr_native_value = next_first.date()
            self._attr_extra_state_attributes = {
                "solar_date": next_first.strftime("%d/%m/%Y"),
                "lunar_month": next_month,
                "lunar_year": next_year,
                "days_until": (next_first.date() - now.date()).days,
            }


class NextLunarFifteenthSensor(LunarBaseSensor):
    """Sensor for the next 15th of the lunar month (solar date)."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        super().__init__(hass, "Rằm kế tiếp", "next_lunar_fifteenth")
        self._attr_icon = "mdi:moon-full"
        self._attr_device_class = SensorDeviceClass.DATE

    async def async_update(self) -> None:
        """Update the sensor."""
        now = datetime.now()
        lunar = solar_to_lunar(now.day, now.month, now.year)
        lunar_day, lunar_month, lunar_year, is_leap = lunar
        
        # Calculate next 15th day
        if lunar_day >= 15:
            # Move to next month's 15th
            target_month = lunar_month + 1
            target_year = lunar_year
            if target_month > 12:
                target_month = 1
                target_year += 1
        else:
            target_month = lunar_month
            target_year = lunar_year
        
        # Convert back to solar
        solar_date = lunar_to_solar(15, target_month, target_year, 0)
        if solar_date[0] != 0:
            next_fifteenth = datetime(solar_date[2], solar_date[1], solar_date[0])
            self._attr_native_value = next_fifteenth.date()
            self._attr_extra_state_attributes = {
                "solar_date": next_fifteenth.strftime("%d/%m/%Y"),
                "lunar_month": target_month,
                "lunar_year": target_year,
                "days_until": (next_fifteenth.date() - now.date()).days,
            }
