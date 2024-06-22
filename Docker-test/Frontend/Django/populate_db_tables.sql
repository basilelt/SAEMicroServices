-- Insert planes
INSERT INTO plane (model, second_class_capacity, first_class_capacity)
SELECT model, second_class_capacity, first_class_capacity FROM (
    SELECT 'Boeing 747' AS model, 300 AS second_class_capacity, 50 AS first_class_capacity
    WHERE NOT EXISTS (SELECT 1 FROM plane WHERE model = 'Boeing 747')
    UNION ALL
    SELECT 'Airbus A380', 400, 70
    WHERE NOT EXISTS (SELECT 1 FROM plane WHERE model = 'Airbus A380')
    UNION ALL
    SELECT 'Boeing 777', 250, 50
    WHERE NOT EXISTS (SELECT 1 FROM plane WHERE model = 'Boeing 777')
    UNION ALL
    SELECT 'Airbus A320', 150, 30
    WHERE NOT EXISTS (SELECT 1 FROM plane WHERE model = 'Airbus A320')
    UNION ALL
    SELECT 'Boeing 737', 120, 20
    WHERE NOT EXISTS (SELECT 1 FROM plane WHERE model = 'Boeing 737')
    UNION ALL
    SELECT 'Airbus A330', 200, 40
    WHERE NOT EXISTS (SELECT 1 FROM plane WHERE model = 'Airbus A330')
) AS subquery;

-- Insert airports
INSERT INTO airport (name, location)
SELECT name, location FROM (
    SELECT 'Los Angeles International Airport' AS name, 'Los Angeles, CA, USA' AS location
    WHERE NOT EXISTS (SELECT 1 FROM airport WHERE name = 'Los Angeles International Airport')
    UNION ALL
    SELECT 'Heathrow Airport', 'London, UK'
    WHERE NOT EXISTS (SELECT 1 FROM airport WHERE name = 'Heathrow Airport')
    UNION ALL
    SELECT 'Charles de Gaulle Airport', 'Paris, France'
    WHERE NOT EXISTS (SELECT 1 FROM airport WHERE name = 'Charles de Gaulle Airport')
    UNION ALL
    SELECT 'Tokyo Haneda Airport', 'Tokyo, Japan'
    WHERE NOT EXISTS (SELECT 1 FROM airport WHERE name = 'Tokyo Haneda Airport')
    UNION ALL
    SELECT 'Beijing Capital International Airport', 'Beijing, China'
    WHERE NOT EXISTS (SELECT 1 FROM airport WHERE name = 'Beijing Capital International Airport')
    UNION ALL
    SELECT 'Dubai International Airport', 'Dubai, UAE'
    WHERE NOT EXISTS (SELECT 1 FROM airport WHERE name = 'Dubai International Airport')
    UNION ALL
    SELECT 'Frankfurt Airport', 'Frankfurt, Germany'
    WHERE NOT EXISTS (SELECT 1 FROM airport WHERE name = 'Frankfurt Airport')
    UNION ALL
    SELECT 'John F. Kennedy International Airport', 'New York, NY, USA'
    WHERE NOT EXISTS (SELECT 1 FROM airport WHERE name = 'John F. Kennedy International Airport')
    UNION ALL
    SELECT 'Singapore Changi Airport', 'Singapore'
    WHERE NOT EXISTS (SELECT 1 FROM airport WHERE name = 'Singapore Changi Airport')
    UNION ALL
    SELECT 'Amsterdam Schiphol Airport', 'Amsterdam, Netherlands'
    WHERE NOT EXISTS (SELECT 1 FROM airport WHERE name = 'Amsterdam Schiphol Airport')
) AS subquery;

-- Insert tracks
INSERT INTO track (track_number, length, airport_id)
SELECT track_number, length, airport_id FROM (
    SELECT 'T1' AS track_number, 4000 AS length, 1 AS airport_id
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T1')
    UNION ALL
    SELECT 'T2', 3500, 1
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T2')
    UNION ALL
    SELECT 'T3', 3000, 2
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T3')
    UNION ALL
    SELECT 'T4', 2500, 2
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T4')
    -- ... and so on for the remaining tracks
) AS subquery;

-- Insert staff types
INSERT INTO staff_type (type)
SELECT type FROM (
    SELECT 'Pilot' AS type
    WHERE NOT EXISTS (SELECT 1 FROM staff_type WHERE type = 'Pilot')
    UNION ALL
    SELECT 'Co-Pilot'
    WHERE NOT EXISTS (SELECT 1 FROM staff_type WHERE type = 'Co-Pilot')
    UNION ALL
    SELECT 'Flight Attendant'
    WHERE NOT EXISTS (SELECT 1 FROM staff_type WHERE type = 'Flight Attendant')
    UNION ALL
    SELECT 'Ground Crew'
    WHERE NOT EXISTS (SELECT 1 FROM staff_type WHERE type = 'Ground Crew')
    UNION ALL
    SELECT 'Maintenance Engineer'
    WHERE NOT EXISTS (SELECT 1 FROM staff_type WHERE type = 'Maintenance Engineer')
) AS subquery;

-- Insert flights
INSERT INTO flight (flight_number, departure, arrival, plane_id, track_origin_id, track_destination_id)
SELECT flight_number, departure::timestamp with time zone, arrival::timestamp with time zone, plane_id, track_origin_id, track_destination_id FROM (
    SELECT 'FL1001' AS flight_number, '2023-01-01 06:00:00' AS departure, '2023-01-01 09:00:00' AS arrival, 1 AS plane_id, 1 AS track_origin_id, 2 AS track_destination_id
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1001')
    UNION ALL
    SELECT 'FL1002', '2023-01-02 07:00:00', '2023-01-02 10:00:00', 2, 3, 4
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1002')
    -- ... and so on for the remaining flights
) AS subquery;