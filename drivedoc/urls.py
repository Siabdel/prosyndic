
from django.urls import path, include
from drivedoc import views
from drivedoc import views as pro_view
from drivedoc.views import DocumentListCreateView, read_document, render_pdf

urlpatterns = [
 ## API Documents 
    path('api/documents/', pro_view.DocumentListCreateView.as_view(), name='document-list-create'),
    path('read-document/<int:document_id>/',pro_view.read_document, name='read-document'),
    path('api/documents/<int:document_id>/pdf/', render_pdf, name='render-pdf'),
    path('api/documents/', DocumentListCreateView.as_view(), name='document-list-create'),
]

