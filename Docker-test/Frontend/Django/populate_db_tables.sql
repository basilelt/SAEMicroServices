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
    UNION ALL
    SELECT 'T5', 2000, 3
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T5')
    UNION ALL
    SELECT 'T6', 1500, 3
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T6')
    UNION ALL
    SELECT 'T7', 1000, 4
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T7')
    UNION ALL
    SELECT 'T8', 500, 4
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T8')
    UNION ALL
    SELECT 'T9', 4000, 5
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T9')
    UNION ALL
    SELECT 'T10', 3500, 5
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T10')
    UNION ALL
    SELECT 'T11', 3000, 6
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T11')
    UNION ALL
    SELECT 'T12', 2500, 6
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T12')
    UNION ALL
    SELECT 'T13', 2000, 7
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T13')
    UNION ALL
    SELECT 'T14', 1500, 7
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T14')
    UNION ALL
    SELECT 'T15', 1000, 8
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T15')
    UNION ALL
    SELECT 'T16', 500, 8
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T16')
    UNION ALL
    SELECT 'T17', 1800, 9
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T17')
    UNION ALL
    SELECT 'T18', 1600, 9
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T18')
    UNION ALL
    SELECT 'T19', 1400, 10
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T19')
    UNION ALL
    SELECT 'T20', 1200, 10
    WHERE NOT EXISTS (SELECT 1 FROM track WHERE track_number = 'T20')
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
    SELECT 'FL1001' AS flight_number, '2023-01-01 06:00:00' AS departure, '2023-01-01 09:00:00' AS arrival, 1 AS plane_id, 1 AS track_origin_id, 9 AS track_destination_id
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1001')
    UNION ALL
    SELECT 'FL1002', '2023-01-02 08:00:00', '2023-01-02 11:00:00', 2, 3, 10
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1002')
    UNION ALL
    SELECT 'FL1003', '2023-01-03 10:00:00', '2023-01-03 13:00:00', 3, 1, 5
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1003')
    UNION ALL
    SELECT 'FL1004', '2023-01-04 12:00:00', '2023-01-04 15:00:00', 4, 2, 6
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1004')
    UNION ALL
    SELECT 'FL1005', '2023-01-05 14:00:00', '2023-01-05 17:00:00', 5, 3, 7
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1005')
    UNION ALL
    SELECT 'FL1006', '2023-01-06 16:00:00', '2023-01-06 19:00:00', 6, 4, 8
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1006')
    UNION ALL
    SELECT 'FL1007', '2023-01-07 18:00:00', '2023-01-07 21:00:00', 1, 5, 9
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1007')
    UNION ALL
    SELECT 'FL1008', '2023-01-08 20:00:00', '2023-01-08 23:00:00', 2, 6, 10
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1008')
    UNION ALL
    SELECT 'FL1009', '2023-01-09 22:00:00', '2023-01-10 01:00:00', 3, 7, 1
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1009')
    UNION ALL
    SELECT 'FL1010', '2023-01-10 00:00:00', '2023-01-10 03:00:00', 4, 8, 2
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1010')
    UNION ALL
    SELECT 'FL1011', '2023-01-11 02:00:00', '2023-01-11 05:00:00', 5, 9, 3
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1011')
    UNION ALL
    SELECT 'FL1012', '2023-01-12 04:00:00', '2023-01-12 07:00:00', 6, 10, 4
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1012')
    UNION ALL
    SELECT 'FL1013', '2023-01-13 06:00:00', '2023-01-13 09:00:00', 1, 1, 5
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1013')
    UNION ALL
    SELECT 'FL1014', '2023-01-14 08:00:00', '2023-01-14 11:00:00', 2, 2, 6
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1014')
    UNION ALL
    SELECT 'FL1015', '2023-01-15 10:00:00', '2023-01-15 13:00:00', 3, 3, 7
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1015')
    UNION ALL
    SELECT 'FL1016', '2023-01-16 12:00:00', '2023-01-16 15:00:00', 4, 4, 8
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1016')
    UNION ALL
    SELECT 'FL1017', '2023-01-17 14:00:00', '2023-01-17 17:00:00', 5, 5, 9
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1017')
    UNION ALL
    SELECT 'FL1018', '2023-01-18 16:00:00', '2023-01-18 19:00:00', 6, 6, 10
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1018')
    UNION ALL
    SELECT 'FL1019', '2023-01-19 18:00:00', '2023-01-19 21:00:00', 1, 7, 1
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1019')
    UNION ALL
    SELECT 'FL1020', '2023-01-20 20:00:00', '2023-01-20 23:00:00', 2, 8, 2
    WHERE NOT EXISTS (SELECT 1 FROM flight WHERE flight_number = 'FL1020')
) AS subquery;

-- Insert booking_types
INSERT INTO booking_type (type, price)
SELECT type, price FROM (
    SELECT 'Second Class' AS type, 100 AS price
    WHERE NOT EXISTS (SELECT 1 FROM booking_type WHERE type = 'Second Class')
    UNION ALL
    SELECT 'First Class', 200
    WHERE NOT EXISTS (SELECT 1 FROM booking_type WHERE type = 'First Class')
) AS subquery;