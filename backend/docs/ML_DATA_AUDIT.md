# ML Data Audit

This document summarizes the current state of the backend models and database tables, identifying the data entities that are available for the ML Intelligence Layer.

## Entities Audited

The existing repository (inside `app/models`) contains the following entities:

1. **Asset (`assets`)**
   - Contains physical railway infrastructure (e.g., track, signal, OHE).
   - Key Fields: `id`, `asset_code`, `asset_type`, `name`, `location`, `status`, `commissioned_date`, `last_maintenance_date`, `next_maintenance_due`.

2. **MaintenanceTask (`maintenance_task`)**
   - The primary entity representing work that needs to be scheduled.
   - Key Fields: `id`, `asset_id`, `maintenance_type`, `description`, `priority`, `required_duration_minutes`, `earliest_start`, `latest_finish`, `deadline`, `required_crew_type`, `status`, `safety_clearance_required`.

3. **Section (`sections`)**
   - The geographical region of tracks between two stations.
   - Key Fields: `id`, `section_code`, `name`, `from_station_id`, `to_station_id`, `distance_km`, `number_of_tracks`, `electrified`, `maximum_speed`, `capacity`, `status`, `maintenance_allowed`.

4. **Block (`blocks`)**
   - Scheduled maintenance windows that occupy sections of track.
   - Key Fields: `id`, `maintenance_task_id`, `section_id`, `planned_start`, `planned_end`, `actual_start`, `actual_end`, `status`, `priority`, `reason`.

5. **Train (`trains`)**
   - Rolling stock traveling along the network.
   - Key Fields: `id`, `train_number`, `train_name`, `train_type`, `priority`, `origin_station_id`, `destination_station_id`, `rake_id`, `locomotive_id`, `status`, `delay_minutes`.

6. **TrainSchedule (`train_schedules`)**
   - Instances of trains on a specific date and their expected/actual timings.
   - Key Fields: `id`, `train_id`, `service_date`, `scheduled_departure`, `scheduled_arrival`, `actual_departure`, `actual_arrival`, `status`, `delay_minutes`.

## Summary
The backend successfully represents the foundational objects needed for the SIH 26027 block planning engine. All required relationships between `MaintenanceTask`, `Asset`, `Section`, and `Block` are present. 

Some ML-specific features (such as `historical_failure_count` on `Asset`) are currently missing from the raw schemas and will need to be derived or represented synthetically for the ML Phase.
