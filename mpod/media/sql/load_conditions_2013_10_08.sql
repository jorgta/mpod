BEGIN;
DELETE FROM data_experimentalparcond;
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_conditions_frequency', '_conditions_frequency', 'NULL', 'NULL', 'NULL');
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_conditions_magnetic_field', '_conditions_magnetic_field', 'NULL', 'NULL', 'NULL');
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_conditions_pressure', '_conditions_pressure', 'NULL', 'NULL', 'NULL');
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_conditions_reference_temperature_thermoelastic_non_linear_fit', '_conditions_reference_temperature_thermoelastic_non_linear_fit', 'NULL', 'NULL', 'NULL');
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_conditions_temperature', '_conditions_temperature', 'NULL', 'NULL', 'NULL');
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_conditions_temperature_cycle', '_conditions_temperature_cycle', 'NULL', 'NULL', 'NULL');
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_conditions_temperature_range_begin', '_conditions_temperature_range_begin', 'NULL', 'NULL', 'NULL');
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_conditions_temperature_range_end', '_conditions_temperature_range_end', 'NULL', 'NULL', 'NULL');
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_conditions_wavelength', '_conditions_wavelength', 'NULL', 'NULL', 'NULL');
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_frame', '_frame', 'NULL', 'NULL', 'NULL');
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_measurement_method', '_measurement_method', 'NULL', 'NULL', 'NULL');
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_measurement_poling', '_measurement_poling', 'NULL', 'NULL', 'NULL');
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_symmetry_point_group_name_H-M', '_symmetry_point_group_name_H-M', 'NULL', 'NULL', 'NULL');
UPDATE data_experimentalparcond SET name = 'conditions frequency'WHERE tag = '_prop_conditions_frequency';
UPDATE data_experimentalparcond SET units = 's^-1'WHERE tag = '_prop_conditions_frequency';
UPDATE data_experimentalparcond SET units_detail = 'hertz'WHERE tag = '_prop_conditions_frequency';
UPDATE data_experimentalparcond SET name = 'conditions magnetic field'WHERE tag = '_prop_conditions_magnetic_field';
UPDATE data_experimentalparcond SET units = 'T'WHERE tag = '_prop_conditions_magnetic_field';
UPDATE data_experimentalparcond SET units_detail = 'tesla'WHERE tag = '_prop_conditions_magnetic_field';
UPDATE data_experimentalparcond SET name = 'conditions pressure'WHERE tag = '_prop_conditions_pressure';
UPDATE data_experimentalparcond SET units = 'Pa'WHERE tag = '_prop_conditions_pressure';
UPDATE data_experimentalparcond SET units_detail = 'pascal'WHERE tag = '_prop_conditions_pressure';
UPDATE data_experimentalparcond SET name = 'conditions reference temperature thermoelastic non linear fit'WHERE tag = '_prop_conditions_reference_temperature_thermoelastic_non_linear_fit';
UPDATE data_experimentalparcond SET units = 'K'WHERE tag = '_prop_conditions_reference_temperature_thermoelastic_non_linear_fit';
UPDATE data_experimentalparcond SET units_detail = 'kelvin'WHERE tag = '_prop_conditions_reference_temperature_thermoelastic_non_linear_fit';
UPDATE data_experimentalparcond SET name = 'conditions temperature'WHERE tag = '_prop_conditions_temperature';
UPDATE data_experimentalparcond SET units = 'K'WHERE tag = '_prop_conditions_temperature';
UPDATE data_experimentalparcond SET units_detail = 'kelvin'WHERE tag = '_prop_conditions_temperature';
UPDATE data_experimentalparcond SET name = 'conditions temperature cycle'WHERE tag = '_prop_conditions_temperature_cycle';
UPDATE data_experimentalparcond SET units = '1'WHERE tag = '_prop_conditions_temperature_cycle';
UPDATE data_experimentalparcond SET units_detail = 'pure number'WHERE tag = '_prop_conditions_temperature_cycle';
UPDATE data_experimentalparcond SET name = 'conditions temperature range begin'WHERE tag = '_prop_conditions_temperature_range_begin';
UPDATE data_experimentalparcond SET units = 'K'WHERE tag = '_prop_conditions_temperature_range_begin';
UPDATE data_experimentalparcond SET units_detail = 'kelvin'WHERE tag = '_prop_conditions_temperature_range_begin';
UPDATE data_experimentalparcond SET name = 'conditions temperature range end'WHERE tag = '_prop_conditions_temperature_range_end';
UPDATE data_experimentalparcond SET units = 'K'WHERE tag = '_prop_conditions_temperature_range_end';
UPDATE data_experimentalparcond SET units_detail = 'kelvin'WHERE tag = '_prop_conditions_temperature_range_end';
UPDATE data_experimentalparcond SET name = 'conditions wavelength'WHERE tag = '_prop_conditions_wavelength';
UPDATE data_experimentalparcond SET units = '10^-6.metre'WHERE tag = '_prop_conditions_wavelength';
UPDATE data_experimentalparcond SET units_detail = 'micrometre'WHERE tag = '_prop_conditions_wavelength';
UPDATE data_experimentalparcond SET name = 'frame'WHERE tag = '_prop_frame';
UPDATE data_experimentalparcond SET units = 'n.a.'WHERE tag = '_prop_frame';
UPDATE data_experimentalparcond SET units_detail = 'n.a.'WHERE tag = '_prop_frame';
UPDATE data_experimentalparcond SET name = 'measurement method'WHERE tag = '_prop_measurement_method';
UPDATE data_experimentalparcond SET units = 'n.a.'WHERE tag = '_prop_measurement_method';
UPDATE data_experimentalparcond SET units_detail = 'n.a.'WHERE tag = '_prop_measurement_method';
UPDATE data_experimentalparcond SET name = 'measurement poling'WHERE tag = '_prop_measurement_poling';
UPDATE data_experimentalparcond SET units = 'n.a.'WHERE tag = '_prop_measurement_poling';
UPDATE data_experimentalparcond SET units_detail = 'n.a.'WHERE tag = '_prop_measurement_poling';
UPDATE data_experimentalparcond SET name = 'symmetry point group name H-M'WHERE tag = '_prop_symmetry_point_group_name_H-M';
UPDATE data_experimentalparcond SET units = 'n.a.'WHERE tag = '_prop_symmetry_point_group_name_H-M';
UPDATE data_experimentalparcond SET units_detail = 'n.a.'WHERE tag = '_prop_symmetry_point_group_name_H-M';
COMMIT;
