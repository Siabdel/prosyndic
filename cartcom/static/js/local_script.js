
			var i = 0;
			var i_gf = 0;
			var id_gd_barre = 0;
			// barre de progression
			function gf_barre(){
			  i_gf++;
			  console.log("on barre progress ..." + i_gf);
			  if (i_gf >= 5) {
			    clearInterval(id_gd_barre);
			    console.log("on arrete ...");
			  }
			}
 
