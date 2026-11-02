# BrAPI-GenX — SensorDevice

SensorDevice records describe SensorDevice entries.
BrAPI v2.1 has no SensorDevice record.

- `POST /genx/v1/sensor-devices` (`genxRegisterSensorDevice`) registers one
  `SensorDevice` (`Schemas/SensorDeviceNewRequest.yaml`). Same
  `sensorDeviceDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/sensor-devices` (`genxListSensorDevices`) lists records,
  optionally filtered by status.
- `GET /genx/v1/sensor-devices/{sensorDeviceDbId}`
  (`genxGetSensorDevice`) retrieves one record.

Details and falsifiers: `../RFC-149-SensorDevice.md`.
