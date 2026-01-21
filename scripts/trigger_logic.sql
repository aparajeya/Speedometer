CREATE OR REPLACE FUNCTION notify_vehicle_speed()
RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify(
        'vehicle_speed_channel',
        json_build_object(
            'time', NEW.time,
            'speed_kmh', NEW.speed_kmh
        )::text
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Below is the trigger creation statement. Uncomment to create the trigger.
-- DROP TRIGGER IF EXISTS vehicle_speed_notify_trigger ON vehicle_speed;

-- CREATE TRIGGER vehicle_speed_notify_trigger
-- AFTER INSERT ON vehicle_speed
-- FOR EACH ROW
-- EXECUTE FUNCTION notify_vehicle_speed();
