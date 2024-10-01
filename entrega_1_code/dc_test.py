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

    # Método para probar una distancia válida en kilómetros
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

    # Método para probar una distancia válida en millas náuticas
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

    # Método para probar una unidad inválida
    #def test_invalid_unit(self):
    #    message = pb2.SourceDest(
    #        source=pb2.Position(latitude=-33.0351516, longitude=-70.5955963),
    #        destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
    #        unit="invalid_unit"
    #    )
    #    response = self.stub.geodesic_distance(message)
    #    response_data = json.loads(MessageToJson(response))

    #    self.assertEqual(response_data["distance"], -1)
    #    self.assertEqual(response_data["unit"], "invalid")

    # Método para probar una latitud en frontera (-90)
    def test_boundary_latitude_min(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-90, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertGreater(response_data["distance"], 0)

    # Método para probar una latitud en frontera (90)
    def test_boundary_latitude_max(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=90, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertGreater(response_data["distance"], 0)

    # Método para probar una longitud en frontera (-180)
    def test_boundary_longitude_min(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=-180),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit=""
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertGreater(response_data["distance"], 0)

    # Método para probar una longitud en frontera (180)
    def test_boundary_longitude_max(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=180),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        response_data = json.loads(MessageToJson(response))

        self.assertGreater(response_data["distance"], 0)

    # Método para probar latitud inválida fuera del rango
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

    # Método para probar longitud inválida fuera del rango
    #def test_invalid_longitude(self):
    #    message = pb2.SourceDest(
    #        source=pb2.Position(latitude=-33.0351516, longitude=-190),
    #        destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
    #        unit="km"
    #    )
    #    response = self.stub.geodesic_distance(message)
    #    response_data = json.loads(MessageToJson(response))

    #    self.assertEqual(response_data["distance"], -1)
    #    self.assertEqual(response_data["unit"], "invalid")


# Ejecución de las pruebas
if __name__ == "__main__":
    unittest.main()
