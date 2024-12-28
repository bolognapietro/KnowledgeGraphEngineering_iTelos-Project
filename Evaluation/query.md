# Evaluation of Competency Questions

### CQ1: Luca inquires about available padel courts in Trento after 7 PM.

```sparql
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
```

### CQ2: Luca also asks if there are any padel events during the weekend of the Festival dello Sport.
```sparql
PREFIX etype: <http://knowdive.disi.unitn.it/etype#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?event_name ?address ?municipality
WHERE {
  
  # Match Event and Organization
  ?event rdf:type etype:Event_UKC-56 ;
         etype:identification_UKC-36247 ?event_id ;
         etype:name_UKC-2 ?event_name .
  
  ?organise etype:organise_UKC-104711 ?event ;
            etype:identification_UKC-36247 ?organise_organization_id .
  
  ?organization rdf:type etype:Organization_UKC-43416 ;
               etype:identification_UKC-36247 ?organization_id ;
               etype:name_UKC-2 "La Gazzetta dello Sport e Trentino Marketing" .
  
  FILTER(?organise_organization_id = ?organization_id)

  # Match the Sport
  ?based_on etype:basedOn_UKC-92536 ?event ;
            etype:identification_UKC-36247 ?based_on_sport_id .
  
  ?sport rdf:type etype:Sport_UKC-2593 ;
         etype:identification_UKC-36247 ?sport_id ;
         etype:name_UKC-2 ?sport_name .
  
  FILTER(?based_on_sport_id = ?sport_id && ?sport_id = "136")
    
  # Match Event's Location
  ?placed etype:placed_UKC-85982 ?event ;
          etype:identification_UKC-36247 ?location_id .
  
  ?location rdf:type etype:Location_UKC-695 ;
            etype:identification_UKC-36247 ?location_id ;
            etype:address_UKC-45004 ?address ;
            etype:municipality_UKC-45537 ?municipality .
}
```

### CQ3: Luca asks if there will be events in Trentino that have Sara Errani as a guest.
```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX etype: <http://knowdive.disi.unitn.it/etype#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?name ?startDate ?endDate ?address ?municipality
WHERE {
  # Filter early for guests named "Sara Errani"
  ?guest rdf:type <http://knowdive.disi.unitn.it/etype#Guest_KGE24-SportFacilities&SportEvents-8001> ;
         etype:identification_UKC-36247 ?guest_id ;
         etype:given_name_UKC-33531 "Sara" ;
         etype:family_name_UKC-33528 "Errani" .
         
  # Match events involving the guest
  ?appear etype:appear_UKC-101132 ?event ;
          etype:identification_UKC-36247 ?guest_id .
  
  # Get events and optional end dates
  ?event rdf:type etype:Event_UKC-56 ;
         etype:name_UKC-2 ?name ;
         etype:startDate_schema.org-startDate ?startDate .
  
  OPTIONAL {
    ?event etype:endDate_schema.org-endDate ?endDate .
  }
  
  # Match event location
  ?placed etype:placed_UKC-85982 ?event ;
          etype:identification_UKC-36247 ?location_id .
  
  ?location rdf:type etype:Location_UKC-695 ;
            etype:identification_UKC-36247 ?location_id ;
            etype:address_UKC-45004 ?address ;
            etype:municipality_UKC-45537 ?municipality .
}
```

### CQ4: Anna wants to know what sports can be practiced in Trentino.
```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX etype: <http://knowdive.disi.unitn.it/etype#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?name
WHERE {
    
    # Get Facilities
    ?facility rdf:type etype:Facility_UKC-17619 .
     
    # Get associated sports
  ?have etype:have_UKC-103527 ?facility ;
      etype:identification_UKC-36247 ?have_sport_id .
    
    ?sport rdf:type etype:Sport_UKC-2593 ;
      etype:identification_UKC-36247 ?sport_id ;
      etype:name_UKC-2 ?name .
    
    FILTER(?have_sport_id = ?sport_id)
}
```

### CQ5: Spending the weekend with friends in Folgaria, Anna asks if there are any lighted volleyball or beach volleyball courts available throughout the day.
```sparql

```

### CQ6: As a volleyball enthusiast, Anna would like to know if there will be any volleyball events during the summer holidays of 2024.
```sparql

```

### CQ7: Matteo also wants to know if there are any skiing events held in Stelvio National Park during the winter season.
```sparql

```

### CQ8: Not finding what he’s looking for, Matteo asks if there are any sport events during his vacation in Trentino.
```sparql

```

### CQ9: A visitor asks Camilla about the events happening today, October 10, at the Festival dello Sport.
```sparql

```

### CQ10: While volunteering at the Festival dello Sport, Camilla becomes interested in tennis and wants to know if there are any tennis-related events and if tennis courts are available when she returns to Molveno for the weekend.
```sparql

```

