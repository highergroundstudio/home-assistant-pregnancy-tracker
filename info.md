# Pregnancy Tracker for Home Assistant

A privacy-focused custom integration that helps you track pregnancy progress entirely inside Home Assistant - because if Home Assistant can track your pool temperature, it can track this too! 🤰

## What You Get

This integration creates **7 sensors** to track your pregnancy:

- 📅 **Weeks** - Current week of pregnancy (with days into week)
- ⏱️ **Days Elapsed** - Total days since pregnancy start
- ⏰ **Days Remaining** - Days until due date
- 📊 **Percent Complete** - How far along you are
- 📈 **Trimester** - Which trimester (1, 2, or 3)
- ℹ️ **Status** - Current status (Just Started, In Progress, Due Today, Overdue)
- 🥕 **Size Comparison** - Fun comparisons to help visualize baby's size

## Privacy First

- ✅ 100% local calculations
- ✅ No internet connection required
- ✅ No cloud services or APIs
- ✅ No data leaves your Home Assistant
- ✅ No tracking or analytics

## Fun Size Comparisons

Choose between two comparison modes:

### 🥬 Veggie Mode
Classic fruit and vegetable comparisons
- Week 8: Raspberry
- Week 20: Banana  
- Week 40: Small pumpkin

### 👨 Dad Mode
Items dads can relate to
- Week 8: Dad's golf tee
- Week 20: Dad's laptop charger
- Week 40: Dad's grill

## Easy Setup

Just enter:
1. Your due date (YYYY-MM-DD format)
2. Pregnancy length (optional, defaults to 280 days)
3. Comparison mode (veggie or dad)

That's it! All sensors will appear and update automatically.

## Use Cases

- Display on your dashboard
- Create automations for milestones
- Send notifications for trimester changes
- Share progress with family (your choice!)
- Track multiple pregnancies (each gets its own device)

## Example Automations

```yaml
# Get notified when entering a new trimester
automation:
  - alias: "New Trimester Alert"
    trigger:
      platform: state
      entity_id: sensor.pregnancy_tracker_trimester
    action:
      service: notify.mobile_app
        data:
          message: "Welcome to trimester {{ states('sensor.pregnancy_tracker_trimester') }}! 🎉"
```

Enjoy tracking your pregnancy journey! 💕
