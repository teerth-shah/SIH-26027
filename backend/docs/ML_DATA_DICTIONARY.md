# ML Data Dictionary

This data dictionary outlines the available backend operational data and how it maps to machine learning features. It includes available fields, derivable fields, and explicitly identifies missing data.

## 1. Asset (`assets`)

| Field | Data Type | Meaning | Source | Required? | Used by ML? | Feature Status |
|-------|-----------|---------|--------|-----------|-------------|----------------|
| `id` | Integer | Primary key | Backend | Yes | No | Available |
| `asset_code` | String | Unique identifier for asset | Backend | Yes | No | Available |
| `asset_type` | String | Type of asset (e.g., Signal, Track) | Backend | Yes | Yes (categorical) | Available |
| `name` | String | Human readable name | Backend | No | No | Available |
| `location` | String | Asset physical location | Backend | No | Yes (geospatial/categorical) | Available |
| `status` | String | Operational status | Backend | No | Yes (state) | Available |
| `commissioned_date` | Date | Date asset was installed | Backend | No | Yes (derivable) | Available |
| `last_maintenance_date`| Date | Last time work was performed | Backend | No | Yes (derivable) | Available |
| `next_maintenance_due` | Date | When maintenance is scheduled | Backend | No | Yes (derivable) | Available |

**Features derivable from Asset:**
- `asset_age` (current_date - `commissioned_date`)
- `days_since_last_maintenance` (current_date - `last_maintenance_date`)

**MISSING FROM CURRENT BACKEND:**
- `criticality` (integer rating of asset importance)
- `failure_count` (historical failure records)
- `section_id` (direct foreign key linking asset to a section)

## 2. MaintenanceTask (`maintenance_task`)

| Field | Data Type | Meaning | Source | Required? | Used by ML? | Feature Status |
|-------|-----------|---------|--------|-----------|-------------|----------------|
| `id` | Integer | Primary key | Backend | Yes | No | Available |
| `asset_id` | Integer | FK to `assets` | Backend | Yes | Yes (join key) | Available |
| `maintenance_type` | String | Type of work | Backend | Yes | Yes (categorical) | Available |
| `description` | String | Notes/description | Backend | No | No (NLP potential) | Available |
| `priority` | Integer | Urgency (1-10) | Backend | No | Yes | Available |
| `required_duration_minutes`| Integer | How long work takes | Backend | Yes | Yes | Available |
| `earliest_start` | DateTime| Window start | Backend | No | Yes | Available |
| `latest_finish` | DateTime| Window end | Backend | No | Yes | Available |
| `deadline` | DateTime| Mandatory finish | Backend | No | Yes (derivable) | Available |
| `required_crew_type`| String | Department/skills | Backend | No | Yes (categorical) | Available |
| `status` | String | Task status | Backend | No | Yes (filtering) | Available |
| `safety_clearance_required`| Boolean| Does it need clearance | Backend | No | Yes (constraint) | Available |

**Features derivable from MaintenanceTask:**
- `days_until_deadline` (`deadline` - current_date)
- `days_overdue` (current_date - `deadline`, if positive)

**MISSING FROM CURRENT BACKEND:**
- `severity` (currently uses `priority`, but severity of condition is missing)
- `section_id` (Task does not have section; it must be derived via asset, but asset lacks it too)

## 3. Section (`sections`)

| Field | Data Type | Meaning | Source | Required? | Used by ML? | Feature Status |
|-------|-----------|---------|--------|-----------|-------------|----------------|
| `id` | Integer | Primary key | Backend | Yes | Yes (join key)| Available |
| `section_code` | String | Unique string ID | Backend | Yes | No | Available |
| `distance_km` | Float | Length of track | Backend | No | Yes | Available |
| `number_of_tracks`| Integer | Single/double line | Backend | No | Yes | Available |
| `electrified` | Boolean | Has OHE | Backend | No | Yes | Available |
| `maximum_speed` | Float | Track speed limit | Backend | No | Yes | Available |
| `capacity` | Integer | Trains per day | Backend | No | Yes | Available |

## 4. Train (`trains`)

| Field | Data Type | Meaning | Source | Required? | Used by ML? | Feature Status |
|-------|-----------|---------|--------|-----------|-------------|----------------|
| `id` | Integer | Primary key | Backend | Yes | No | Available |
| `train_number` | String | External train ID | Backend | Yes | No | Available |
| `train_type` | String | Goods vs Passenger | Backend | No | Yes (categorical) | Available |
| `priority` | Integer | Traffic importance | Backend | No | Yes | Available |

## 5. Block (`blocks`)

| Field | Data Type | Meaning | Source | Required? | Used by ML? | Feature Status |
|-------|-----------|---------|--------|-----------|-------------|----------------|
| `id` | Integer | Primary key | Backend | Yes | No | Available |
| `maintenance_task_id`| Integer| FK to Task | Backend | Yes | Yes (join key) | Available |
| `section_id` | Integer | FK to Section | Backend | Yes | Yes (join key) | Available |
| `planned_start` | DateTime| Block start | Backend | Yes | Yes | Available |
| `planned_end` | DateTime| Block end | Backend | Yes | Yes | Available |

## 6. TrainSchedule (`train_schedules`)

| Field | Data Type | Meaning | Source | Required? | Used by ML? | Feature Status |
|-------|-----------|---------|--------|-----------|-------------|----------------|
| `id` | Integer | Primary key | Backend | Yes | No | Available |
| `train_id` | Integer | FK to Train | Backend | Yes | Yes (join key) | Available |
| `scheduled_departure`| DateTime| Expected start | Backend | No | Yes (overlap) | Available |
| `scheduled_arrival`| DateTime| Expected finish | Backend | No | Yes (overlap) | Available |

**MISSING FROM CURRENT BACKEND:**
- `section_id` (Schedule does not specify which section the train is on during these times)
