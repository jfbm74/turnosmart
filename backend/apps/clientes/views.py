# clientes/views.py

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ClienteSerializer, ClienteListSerializer
from .models import Cliente


class ClienteListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: ClienteListSerializer(many=True)},
    )
    def get(self, request):
        """
        Obtener la lista de clientes.
        """
        clientes = Cliente.objects.all()
        serializer = ClienteListSerializer(clientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ClienteSerializer,
        responses={
            201: openapi.Response("Cliente creado exitosamente", ClienteSerializer),
            400: "Errores de validación",
        },
    )
    def post(self, request):
        """
        Crear un nuevo cliente.
        """
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Cliente creado exitosamente", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClienteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Cliente.objects.get(pk=pk)
        except Cliente.DoesNotExist:
            return None

    @swagger_auto_schema(
        responses={
            200: ClienteSerializer,
            404: "Cliente no encontrado",
        }
    )
    def get(self, request, pk):
        """
        Obtener los detalles de un cliente por ID.
        """
        cliente = self.get_object(pk)
        if cliente:
            serializer = ClienteSerializer(cliente)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"message": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND
        )

    @swagger_auto_schema(
        request_body=ClienteSerializer,
        responses={
            200: openapi.Response("Cliente editado exitosamente", ClienteSerializer),
            400: "Errores de validación",
            404: "Cliente no encontrado",
        },
    )
    def put(self, request, pk):
        """
        Actualizar los datos de un cliente.
        """
        cliente = self.get_object(pk)
        if cliente:
            serializer = ClienteSerializer(cliente, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Cliente editado exitosamente",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND
        )

    @swagger_auto_schema(
        responses={
            204: "Cliente eliminado exitosamente",
            404: "Cliente no encontrado",
        }
    )
    def delete(self, request, pk):
        """
        Eliminar un cliente.
        """
        cliente = self.get_object(pk)
        if cliente:
            cliente.delete()
            return Response(
                {"message": "Cliente eliminado exitosamente"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"message": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND
        )
