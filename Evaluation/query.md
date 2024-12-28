# Evaluation of Competency Questions

### CQ1: Luca inquires about available padel courts in Trento after 7 PM.

~~~~sql
PREFIX etype: <http://knowdive.disi.unitn.it/etype#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?sport_facility_id ?legalName ?openingHours ?sport_id ?name
WHERE {
  # Match the facility
  ?facility rdf:type etype:Facility_UKC-17619 ;
    etype:identification_UKC-36247 ?sport_facility_id ;
    etype:name_UKC-2 ?legalName .
    
    OPTIONAL { 
        ?facility etype:openingHours_schema.org-openingHours ?openingHours .
    }

  # Match the sport related to the facility
  ?have etype:have_UKC-103527 ?facility ;
    etype:identification_UKC-36247 ?have_sport_id .
  
  ?sport rdf:type etype:Sport_UKC-2593 ;
    etype:identification_UKC-36247 ?sport_id ;
    etype:name_UKC-2 ?name .
            
  FILTER(?have_sport_id = ?sport_id && ?sport_id = "97")
}
~~~~

### CQ2: Luca also asks if there are any padel events during the weekend of the Festival dello Sport.
~~~~sql

~~~~

### CQ3: Luca asks if there will be events in Trentino that have Sara Errani as a guest.
~~~~sql

~~~~

### CQ4: Anna wants to know what sports can be practiced in Trentino.
~~~~sql

~~~~

### CQ5: Spending the weekend with friends in Folgaria, Anna asks if there are any lighted volleyball or beach volleyball courts available throughout the day.
~~~~sql

~~~~

### CQ6: As a volleyball enthusiast, Anna would like to know if there will be any volleyball events during the summer holidays of 2024.
~~~~sql

~~~~

### CQ7: Matteo also wants to know if there are any skiing events held in Stelvio National Park during the winter season.
~~~~sql

~~~~

### CQ8: Not finding what he’s looking for, Matteo asks if there are any sport events during his vacation in Trentino.
~~~~sql

~~~~

### CQ9: A visitor asks Camilla about the events happening today, October 10, at the Festival dello Sport.
~~~~sql

~~~~

### CQ10: While volunteering at the Festival dello Sport, Camilla becomes interested in tennis and wants to know if there are any tennis-related events and if tennis courts are available when she returns to Molveno for the weekend.
~~~~sql

~~~~

