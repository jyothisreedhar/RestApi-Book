from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from .models import Book
from .serializers import BookSerializer, BookModelSerializer, LoginSerializer
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

# Create your views here.
# book create,list,view,update,delete,
# serializeers.py

# function based view
@csrf_exempt
def book_list(request):
    if request.method == "GET":
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def book_details(request, id):
    book = Book.objects.get(id=id)
    if request.method == "GET":
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            # book.book_name=serializer.validated_data.get("book_name")
            # book.author=serializer.validated_data.get("author")
            # book.price=serializer.validated_data.get("price")
            # book.pages=serializer.validated_data.get("pages")
            # book.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        book.delete()
        return JsonResponse({"msg": "deleted"})


# class based view
# book create and booklist
class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookModelSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)

    # create
    def post(self, request):
        serializer = BookModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


# authentication method
# 1.session authentication
# 2.Task authentication
class BookDetailView(APIView):
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]  # (username,password)
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_object(self, id):
        return Book.objects.get(id=id)

    def get(self, request, id):
        book = self.get_object(id)
        serializer = BookModelSerializer(book)
        return JsonResponse(serializer.data, status=201)

    # update method
    def put(self, request, id):
        book = self.get_object(id)
        serializer = BookModelSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    # delete
    def delete(self, request, id):
        book = self.get_object(id)
        book.delete()
        return JsonResponse({"msg": "deleted"})


# Mixin methods
class BookMixinView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # list all book
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # create book
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# update,delete
class BookDetailMixinView(generics.GenericAPIView,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.RetrieveModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class LoginApi(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                token,created=Token.objects.get_or_create(user=user)
                return JsonResponse({"token":token.key})
            else:
                print("no user")
                return JsonResponse({"msg": "failed"})



# app=>settings=>urls=>models=>serializeers=>view
# superuser==>mithun,mithun123
