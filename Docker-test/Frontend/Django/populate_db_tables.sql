-- Insert planes
INSERT INTO plane (model, second_class_capacity, first_class_capacity) VALUES
('Boeing 747', 300, 50),
('Airbus A380', 400, 70),
('Boeing 777', 250, 50),
('Airbus A320', 150, 30),
('Boeing 737', 120, 20),
('Airbus A330', 200, 40);

-- Insert airports
INSERT INTO airport (name, location) VALUES
('Los Angeles International Airport', 'Los Angeles, CA, USA'),
('Heathrow Airport', 'London, UK'),
('Charles de Gaulle Airport', 'Paris, France'),
('Tokyo Haneda Airport', 'Tokyo, Japan'),
('Beijing Capital International Airport', 'Beijing, China'),
('Dubai International Airport', 'Dubai, UAE'),
('Frankfurt Airport', 'Frankfurt, Germany'),
('John F. Kennedy International Airport', 'New York, NY, USA'),
('Singapore Changi Airport', 'Singapore'),
('Amsterdam Schiphol Airport', 'Amsterdam, Netherlands');

-- Insert tracks
INSERT INTO track (track_number, length, airport_id) VALUES
('T1', 4000, 1), ('T2', 3500, 1), ('T3', 3000, 2), ('T4', 2500, 2),
('T5', 4000, 3), ('T6', 3500, 3), ('T7', 3000, 4), ('T8', 2500, 4),
('T9', 4000, 5), ('T10', 3500, 5), ('T11', 3000, 6), ('T12', 2500, 6),
('T13', 4000, 7), ('T14', 3500, 7), ('T15', 3000, 8), ('T16', 2500, 8),
('T17', 4000, 9), ('T18', 3500, 9), ('T19', 3000, 10), ('T20', 2500, 10);

-- Insert booking types
INSERT INTO booking_type (type) VALUES
('second_class'),
('first_class');

-- Insert staff types
INSERT INTO staff_type (type) VALUES
('Pilot'),
('Co-Pilot'),
('Flight Attendant'),
('Ground Crew'),
('Maintenance Engineer');

-- Insert flights
INSERT INTO flight (flight_number, departure, arrival, plane_id, track_origin_id, track_destination_id) VALUES
('FL1001', '2023-01-01 06:00:00', '2023-01-01 09:00:00', 1, 1, 2),
('FL1002', '2023-01-02 07:00:00', '2023-01-02 10:00:00', 2, 3, 4),
('FL1003', '2023-01-03 08:00:00', '2023-01-03 11:00:00', 3, 5, 6),
('FL1004', '2023-01-04 09:00:00', '2023-01-04 12:00:00', 4, 7, 8),
('FL1005', '2023-01-05 10:00:00', '2023-01-05 13:00:00', 5, 9, 10),
('FL1006', '2023-01-06 11:00:00', '2023-01-06 14:00:00', 1, 11, 12),
('FL1007', '2023-01-07 12:00:00', '2023-01-07 15:00:00', 2, 13, 14),
('FL1008', '2023-01-08 13:00:00', '2023-01-08 16:00:00', 3, 15, 16),
('FL1009', '2023-01-09 14:00:00', '2023-01-09 17:00:00', 4, 17, 18),
('FL1010', '2023-01-10 15:00:00', '2023-01-10 18:00:00', 5, 19, 20),
('FL1011', '2023-01-11 06:00:00', '2023-01-11 09:00:00', 1, 2, 1),
('FL1012', '2023-01-12 07:00:00', '2023-01-12 10:00:00', 2, 4, 3),
('FL1013', '2023-01-13 08:00:00', '2023-01-13 11:00:00', 3, 6, 5),
('FL1014', '2023-01-14 09:00:00', '2023-01-14 12:00:00', 4, 8, 7),
('FL1015', '2023-01-15 10:00:00', '2023-01-15 13:00:00', 5, 10, 9),
('FL1016', '2023-01-16 11:00:00', '2023-01-16 14:00:00', 1, 12, 11),
('FL1017', '2023-01-17 12:00:00', '2023-01-17 15:00:00', 2, 14, 13),
('FL1018', '2023-01-18 13:00:00', '2023-01-18 16:00:00', 3, 16, 15),
('FL1019', '2023-01-19 14:00:00', '2023-01-19 17:00:00', 4, 18, 17),
('FL1020', '2023-01-20 15:00:00', '2023-01-20 18:00:00', 5, 20, 19);