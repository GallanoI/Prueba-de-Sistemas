import grpc
import distance_unary_pb2_grpc as pb2_grpc
import distance_unary_pb2 as pb2
import unittest
from google.protobuf.json_format import MessageToJson
import json


# Clase de prueba
class TestDistanceService(unittest.TestCase):

    # Método de configuración para el canal y stub gRPC
    def setUp(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = pb2_grpc.DistanceServiceStub(self.channel)

    # Probar una distancia válida en kilómetros
    def test_valid_km(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertGreater(response_data["distance"], 0)
        self.assertEqual(response_data["unit"], "km")

    # Probar una distancia válida en millas náuticas
    def test_valid_nm(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="nm"
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertGreater(response_data["distance"], 0)
        self.assertEqual(response_data["unit"], "nm")

    # Probar una distancia válida sin unidad de medida
    def test_valid_no_unit(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit=""
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertGreater(response_data["distance"], 0)
        self.assertEqual(response_data["unit"], "km")

    # Probar una unidad inválida
    def test_invalid_unit(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="cm"
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertEqual(response_data["distance"], -1)
        self.assertEqual(response_data["unit"], "invalid")

    # Probar una latitud en frontera (-90)
    def test_boundary_latitude_min(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-90, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertGreater(response_data["distance"], 0)

    # Probar una latitud en frontera (90)
    def test_boundary_latitude_max(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=90, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertGreater(response_data["distance"], 0)

    # Probar una longitud en frontera (-180)
    def test_boundary_longitude_min(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=-180),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit=""
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertGreater(response_data["distance"], 0)

    # Probar una longitud en frontera (180)
    def test_boundary_longitude_max(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=180),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertGreater(response_data["distance"], 0)

    # Probar latitud inválida fuera del rango
    def test_invalid_latitude(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=100, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertEqual(response_data["distance"], -1)
        self.assertEqual(response_data["unit"], "invalid")

    # Probar longitud inválida fuera del rango
    def test_invalid_longitude(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=-190),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertEqual(response_data["distance"], -1)
        self.assertEqual(response_data["unit"], "invalid")

    # Probar valores validos cercanos a valores frontera (~90, ~180)
    def test_near_boundary_values(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=89.9999999, longitude=179.9999999),
            destination=pb2.Position(latitude=-89.9999999, longitude=-179.9999999),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)

        self.assertGreater(response.distance, 0)
        self.assertEqual(response.unit, "km")

    # Probar valores validos cercanos a valores frontera (~-90, ~-180)
    def test_near_negative_boundary_values(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-89.9999999, longitude=-179.9999999),
            destination=pb2.Position(latitude=89.9999999, longitude=179.9999999),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)

        self.assertGreater(response.distance, 0)
        self.assertEqual(response.unit, "km")

    # Probar valores invalidos cercanos a valores frontera (~90, ~180)
    def test_near_boundary_invalid_values(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=90.0000001, longitude=180.0000001),
            destination=pb2.Position(latitude=-90.0000001, longitude=-180.0000001),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)

        self.assertEqual(response.distance, -1.0)
        self.assertEqual(response.unit, "invalid")

    # Probar valores invalidos cercanos a valores frontera (~-90, ~-180)
    def test_near_negative_boundary_invalid_values(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-90.0000001, longitude=-180.0000001),
            destination=pb2.Position(latitude=90.0000001, longitude=180.0000001),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)

        self.assertEqual(response.distance, -1.0)
        self.assertEqual(response.unit, "invalid")

    # Probar una posición incompleta
    def test_incomplete_position(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=10),
            destination=pb2.Position(latitude=20, longitude=30),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)

        self.assertEqual(response.distance, -1.0)
        self.assertEqual(response.unit, "invalid")

    # Probar misma fuente y destino (Distancia 0)
    def test_same_source_and_destination(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=50, longitude=50),
            destination=pb2.Position(latitude=50, longitude=50),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)

        self.assertEqual(response.distance, 0)
        self.assertEqual(response.unit, "km")

    # Probar valores de latitud y longitud intercambiados
    def test_swapped_latitude_longitude(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=180, longitude=90),
            destination=pb2.Position(latitude=-180, longitude=-90),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)

        self.assertEqual(response.distance, -1.0)
        self.assertEqual(response.unit, "invalid")


# Ejecución de las pruebas
if __name__ == "__main__":
    unittest.main()