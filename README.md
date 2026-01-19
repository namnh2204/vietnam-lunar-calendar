# 🌙 Vietnamese Lunar Calendar for Home Assistant

A custom Home Assistant integration that provides Vietnamese lunar calendar (Âm lịch) sensors. Perfect for tracking lunar dates, special days like Mùng 1 (1st) and Rằm (15th), and Vietnamese zodiac information.

## Features

- 📅 **Lunar Date Sensor** - Current lunar date with zodiac information
- 🔢 **Lunar Day/Month/Year Sensors** - Individual date components
- 🌕 **Special Day Detection** - Automatically detects Mùng 1 and Rằm
- 📆 **Next Special Days** - Countdown to next Mùng 1 and Rằm
- 🐉 **Zodiac Information** - Can Chi for year, month, and day

## Installation

### Via HACS (Recommended)

1. Ensure **[HACS](https://hacs.xyz/)** is installed in Home Assistant.
2. Go to **HACS** > **Integrations**.
3. Click the **three dots** in the top right corner and select **Custom repositories**.
4. Paste the repository URL:
   ```text
   https://github.com/namnh2204/vietnamese-lunar-calendar
   ```
5. Select **Integration** as the category.
6. Click **Add**.
7. Close the modal, find "**Vietnamese Lunar Calendar**" in the list, and click **Download**.
8. **Restart** Home Assistant.

### Manual Installation

1. Copy the `vietnamese_lunar_calendar` folder to your Home Assistant `custom_components` directory:
   ```
   custom_components/
   └── vietnamese_lunar_calendar/
       ├── __init__.py
       ├── config_flow.py
       ├── lunar_solar.py
       ├── manifest.json
       ├── sensor.py
       └── strings.json
   ```

2. Restart Home Assistant

### Configuration

1. Go to **Settings** → **Devices & Services** → **+ Add Integration**
2. Search for "**Vietnamese Lunar Calendar**" and add it

## Sensors

After installation, the following sensors will be available:

| Sensor | Entity ID | Description | Example Value |
|--------|-----------|-------------|---------------|
| Ngày Âm Lịch | `sensor.ngay_am_lich` | Full lunar date with zodiac | `1/12 năm Ất Tị` |
| Ngày Âm | `sensor.ngay_am` | Lunar day (1-30) | `1` |
| Tháng Âm | `sensor.thang_am` | Lunar month (1-12) | `12` |
| Năm Âm | `sensor.nam_am` | Lunar year | `2025` |
| Mùng 1 hoặc Rằm | `sensor.mung_1_hoac_ram` | Special day indicator | `Mùng 1` / `Rằm` / `Không` |
| Mùng 1 kế tiếp | `sensor.mung_1_ke_tiep` | Next 1st lunar day (solar date) | `2026-02-17` |
| Rằm kế tiếp | `sensor.ram_ke_tiep` | Next 15th lunar day (solar date) | `2026-02-02` |

### Sensor Attributes

The `sensor.ngay_am_lich` sensor includes these attributes:

| Attribute | Description | Example |
|-----------|-------------|---------|
| `lunar_day` | Lunar day number | `1` |
| `lunar_month` | Lunar month number | `12` |
| `lunar_year` | Lunar year | `2025` |
| `is_leap_month` | Is current month a leap month | `false` |
| `zodiac_year` | Year in Can Chi | `Ất Tị` |
| `zodiac_day` | Day in Can Chi | `Quý Tị` |
| `zodiac_month` | Month in Can Chi | `Kỷ Sửu` |
| `day_of_week` | Vietnamese day of week | `Thứ 2` |
| `solar_date` | Corresponding solar date | `19/01/2026` |

## Example Automations

### Notify on Mùng 1 and Rằm at 6 AM

```yaml
automation:
  - id: lunar_calendar_notification
    alias: "Thông báo Mùng 1 và Rằm"
    description: "Thông báo nhắc nhở vào ngày Mùng 1 và Rằm lúc 6 giờ sáng"
    trigger:
      - platform: time
        at: "06:00:00"
    condition:
      - condition: template
        value_template: >
          {{ states('sensor.mung_1_hoac_ram') in ['Mùng 1', 'Rằm'] }}
    action:
      - service: notify.notify
        data:
          title: "🌙 Nhắc nhở Âm Lịch"
          message: >
            {% if states('sensor.mung_1_hoac_ram') == 'Mùng 1' %}
            Hôm nay là ngày Mùng 1 âm lịch ({{ states('sensor.ngay_am_lich') }}).
            Nhớ thắp hương cúng ông bà tổ tiên! 🙏
            {% else %}
            Hôm nay là ngày Rằm ({{ states('sensor.ngay_am_lich') }}).
            Nhớ thắp hương cúng ông bà tổ tiên! 🙏
            {% endif %}
```

### Notify Before Tết (Lunar New Year)

```yaml
automation:
  - id: tet_countdown
    alias: "Đếm ngược Tết"
    trigger:
      - platform: template
        value_template: >
          {{ state_attr('sensor.mung_1_ke_tiep', 'lunar_month') == 1 
             and state_attr('sensor.mung_1_ke_tiep', 'days_until') == 7 }}
    action:
      - service: notify.notify
        data:
          title: "🎆 Sắp Tết rồi!"
          message: "Còn 7 ngày nữa là Tết Nguyên Đán!"
```

## Dashboard Card Example

### Simple Card (Entities)

```yaml
type: entities
title: 🌙 Âm Lịch
entities:
  - entity: sensor.ngay_am_lich
    name: Ngày Âm Lịch
  - entity: sensor.mung_1_hoac_ram
    name: Ngày Đặc Biệt
  - entity: sensor.ram_ke_tiep
    name: Rằm kế tiếp
  - entity: sensor.mung_1_ke_tiep
    name: Mùng 1 kế tiếp
```

### Custom Button Card

```yaml
type: custom:button-card
entity: sensor.ngay_am_lich
name: "🌙 Âm Lịch"
show_state: true
show_icon: true
icon: mdi:moon-waning-crescent
styles:
  card:
    - border-radius: 12px
    - padding: 16px
  icon:
    - color: purple
  state:
    - font-size: 14px
```

## Technical Details

This integration uses astronomical algorithms from the book "Astronomical Algorithms" by Jean Meeus (1998), adapted from the [SolarLunarCalendar](https://github.com/quangvinh86/SolarLunarCalendar) Python library.

The lunar calendar calculations are specifically tuned for the Vietnamese timezone (UTC+7) and follow the Vietnamese lunar calendar system.

### Timezone

The integration uses Vietnam timezone (UTC+7) by default for all calculations.

## Troubleshooting

### Sensors not appearing

1. Make sure you've restarted Home Assistant after copying the files
2. Check that the integration was added via Settings → Devices & Services
3. Check Home Assistant logs for any error messages

### Wrong lunar date

The lunar calendar uses the Vietnamese timezone (UTC+7). If your Home Assistant timezone is different, there might be a 1-day discrepancy near midnight.

## Credits

- Lunar calendar algorithms: [quangvinh86/SolarLunarCalendar](https://github.com/quangvinh86/SolarLunarCalendar)
- Based on "Astronomical Algorithms" by Jean Meeus, 1998

## License

This integration is provided as-is for personal use with Home Assistant.
