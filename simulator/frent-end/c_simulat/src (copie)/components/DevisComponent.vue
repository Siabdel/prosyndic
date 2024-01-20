
<template>
  <div class="container mt-4">
    <!-- Tableau pour les charges de fonctionnement -->
    <table class="table table-responsive">
      <thead>
        <tr>
          <th scope="col">Rubrique</th>
          <th scope="col">Nom</th>
          <th scope="col">Prix unitaire mensuel</th>
          <th scope="col">Quantité</th>
          <th scope="col">Nombre de mois annuel</th>
          <th scope="col">Montant mensuel</th>
          <th scope="col">Total annuel</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="field in chargesFonctionnementAvecTotal" :key="field.name">
          <td>{{ field.rubrique }}</td>
          <td>{{ field.name }}</td>
          <td>
            <input v-model="field.prixUnitaireMensuel" class="form-control" placeholder="Prix unitaire" />
          </td>
          <td>
            <input v-model="field.quantite" class="form-control" placeholder="Quantité" />
          </td>
          <td>
            <input v-model="field.nombreMoisAnnuel" class="form-control" placeholder="Nombre de mois annuel" />
          </td>

          <td>{{ field.montantMensuel }}</td>
          <td>{{ field.totalAnnuel }}</td>

        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
 data() {
  return {
    chargesFonctionnement: [
      {
        title: "GARDIENNAGE",
        fields: [
          { name: "Jour", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Nuit", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Chef d'équipe", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Maitre Chien", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "ENTRETIEN DES PISCINES",
        fields: [
          { name: "Entretien des Piscines", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "MAITRE NAGEUR",
        fields: [
          { name: "Maitre nageur", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "NETTOYAGE",
        fields: [
          { name: "Femme de Ménage", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Cantonnier", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Produit d'entretien", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Frais collecte dechets", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "ENTRETIEN DES ESPACES VERTS",
        fields: [
          { name: "Chef Jardinier", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Jardinier", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "HYGIENE 3D",
        fields: [
          { name: "Dératisation et Désinsectisation", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "CONSOMMATIONS EAU",
        fields: [
          { name: "Piscines + consom + eau", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Local Syndic + guertie + incendie", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Arrosage", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "CONSOMMATIONS ELECTRICITE",
        fields: [
          { name: "Immeubles", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Piscines + electricite", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Eclairage Ambiance", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Local Syndic + guertie", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "MAINTENANCE",
        fields: [
          { name: "Technicien polyvalent", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Petites réparations", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "FRAIS BANCAIRES",
        fields: [
          { name: "Frais de Banque", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "FRAIS ADMINISTRATIF ET BUREAUTIQUE",
        fields: [
          { name: "Convocation AG", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Frais de justice et Avocat", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
          { name: "Location lieu AG", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "ASSURANCES MULTIRISQUE & RC",
        fields: [
          { name: "Assurance", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "HONORAIRES SYNDIC",
        fields: [
          { name: "Honoraires syndic", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "TOTAL CHARGES DE FONCTIONNEMENT",
        fields: [
          { name: "Provision de prévoyance", prixUnitaireMensuel: 0, quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },
      {
        title: "PROVISION DE PREVOYANCE",
        fields: [
          { name: "Total charges courantes", prixUnitaireMensuel: 0, 
          quantite: 0, nombreMoisAnnuel: 12 },
        ],
      },]
    }
  }
  ,
  
  computed: {
    chargesFonctionnementAvecTotal() {
      //console.log(" total annuel ", this.chargesFonctionnement.fields , field.quantite, montantMensuel)
      return this.chargesFonctionnement.reduce((formattedCharges, rubrique) => {
        return formattedCharges.concat(rubrique.fields.map((field) => {
          const formattedName = field.name.toLowerCase().replace(/\s/g, '_');
          const montantMensuel = field.prixUnitaireMensuel * field.quantite;
          const totalAnnuel = montantMensuel * field.nombreMoisAnnuel;

          return {
            rubrique: rubrique.title,
            name: formattedName,
            prixUnitaireMensuel: field.prixUnitaireMensuel,
            quantite: field.quantite,
            nombreMoisAnnuel: field.nombreMoisAnnuel,
            montantMensuel: montantMensuel,
            totalAnnuel: totalAnnuel,
          };
        }));
      }, []);
    },
  },
};
</script>
