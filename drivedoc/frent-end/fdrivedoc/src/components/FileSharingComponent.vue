
<!-- fileSharingComponent.vue -->
<template>
  <div class="container">
    <div class="row">
      <div class="col-md-4">
        <h2>Documents disponibles XXXX</h2>
        <ul class="list-group">
          <li v-for="document in documents" :key="document.id" class="list-group-item">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <strong>{{ document.title }}</strong>
                <br>
                <small>{{ document.author_username }} - {{ document.fournisseur.nom }}</small>
              </div>
              <button @click="readDocument(document.id)" class="btn btn-primary">Lire</button>
            </div>
          </li>
        </ul>
      </div>

       <div class="col-md-8 mt-3 mt-md-0">
        <div v-if="selectedDocument">
          <h3>{{ selectedDocument.title }}</h3>
          <div class="pdf-container">
            <canvas ref="pdfCanvas"></canvas>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
export default {
  data() {
    return {
      documents: [],
      selectedDocument: null,
      pdfUrl: null,
      pdfInstance: null,
    };
  },
  mounted(){ 
    // Appel à l'API pour récupérer la liste des documents au moment du montage
    this.fetchDocuments();
  },
  methods: {
    fetchDocuments() {
      axios.get('http://localhost:8000/doc/api/documents/')
        .then(response => {
          this.documents = response.data;
        })
        .catch(error => {
          console.error('Erreur lors du chargement des documents', error);
        });
    },
      // Récupérer les détails du document sélectionné depuis l'API
      // Utilisez Axios ou l'API Fetch pour effectuer la requête
      // Mettez à jour selectedDocument avec la réponse
      // Construisez l'URL du document PDF
    readDocument(documentId) {
      const url_pdf = `http://localhost:8000/doc/api/documents/${documentId}/pdf/`

      axios.get(url_pdf)  // Assurez-vous que votre API expose cette route
        .then(response => {
          // Mise à jour des données du document sélectionné et de l'URL du PDF
          this.selectedDocument = document;
          //this.pdfUrl = response.data.pdf_url;
          console.log( " Url du pdf en retour =", response.data.pdf_url);
          this.pdfUrl = url_pdf;

          // Initialiser pdf.js
          this.initPDF();
          // Assurez-vous que votre API renvoie l'URL du PDF
        })
        .catch(error => {
          console.error('Erreur lors de la récupération du document', error);
        });
    },
        ////
    initPDF(){
      // Charger le document PDF
      const pdfPath = this.pdfUrl;  // Assurez-vous que votre API renvoie l'URL du PDF
      const loadingTask = window.pdfjsLib.getDocument(pdfPath);


      loadingTask.promise
        .then(pdf => {
          // Définir le contexte du canevas
          const canvas = this.$refs.pdfCanvas;
          const context = canvas.getContext('2d');

          // Définir la première page à afficher
          // Rendre toutes les pages du PDF
      for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber++) {
        pdf.getPage(pageNumber).then(page => {
          const viewport = page.getViewport({ scale: 1.5 });
          canvas.width = viewport.width;
          canvas.height = viewport.height;

          const renderContext = {
            canvasContext: context,
            viewport: viewport,
          };
          page.render(renderContext);
        });
        }
        })
        .catch(error => {
          console.error('Erreur LoadingTask ## : lors du chargement du document PDF', error);
        });
      },
        /////

    },// fin methods
};
</script>

<style scoped>
/* Ajoutez des styles spécifiques au composant ici si nécessaire */
.pdf-container {
  overflow-y: auto; /* Ajoutez le défilement vertical */
  max-height: 500px; /* ou la hauteur souhaitée */
}
.download
{
    display:none !important;    
}

.print
{
    display:none !important;
}
</style>
