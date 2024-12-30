# Evaluation of Competency Questions

### CQ1: Luca inquires about available padel courts in Trento after 7 PM.

```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX etype: <http://knowdive.disi.unitn.it/etype#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?givenName ?familyName ?legalName ?address ?municipality ?openingHours
WHERE {
  
  ?user rdf:type etype:User_UKC-53492 ;
    	etype:identification_UKC-36247 "1" ;
    	etype:given_name_UKC-33531 ?givenName ;
    	etype:family_name_UKC-33528 ?familyName .

  # Match the facility
  ?facility rdf:type etype:Facility_UKC-17619 ;
            etype:identification_UKC-36247 ?sport_facility_id ;
            etype:name_UKC-2 ?legalName .
  
  # Extract openingHours (if any)
  ?facility etype:openingHours_schema.org-openingHours ?openingHours .
  
  ?have etype:have_UKC-103527 ?facility ;
    etype:identification_UKC-36247 "136" .
    
  # Define a list of days to process
    VALUES (?day ?dayRegex) {
      ("monday"   "monday: (\\d{2}:\\d{2}) - (\\d{2}:\\d{2})")
      ("tuesday"  "tuesday: (\\d{2}:\\d{2}) - (\\d{2}:\\d{2})")
      ("wednesday" "wednesday: (\\d{2}:\\d{2}) - (\\d{2}:\\d{2})")
      ("thursday" "thursday: (\\d{2}:\\d{2}) - (\\d{2}:\\d{2})")
      ("friday"   "friday: (\\d{2}:\\d{2}) - (\\d{2}:\\d{2})")
      ("saturday" "saturday: (\\d{2}:\\d{2}) - (\\d{2}:\\d{2})")
      ("sunday"   "sunday: (\\d{2}:\\d{2}) - (\\d{2}:\\d{2})")
    }

    # Process each day and extract the hours and minutes
    BIND(
        IF(
          REGEX(?openingHours, ?dayRegex, "i"),
          STRDT(SUBSTR(REPLACE(?openingHours, "." + ?day + ": (\\d{2}:\\d{2}) - (\\d{2}:\\d{2}).", "$2"), 1, 2), xsd:integer) * 60,
          false
        ) AS ?hours
    )

    BIND(
        IF(
          REGEX(?openingHours, ?dayRegex, "i"),
          STRDT(SUBSTR(REPLACE(?openingHours, "." + ?day + ": (\\d{2}:\\d{2}) - (\\d{2}:\\d{2}).", "$2"), 4, 2), xsd:integer),
          false
        ) AS ?minutes
    )

    # Check if the total time for the day exceeds 19:00 (1140 minutes)
    BIND(
        IF(
          ?hours + ?minutes >= 1140,
          true,
          false
        ) AS ?exceeds19
    )
  
  # Extract the location of each facility
  ?placed etype:placed_UKC-85982 ?facility ;
          etype:identification_UKC-36247 ?placed_id .
    		  
  ?location rdf:type etype:Location_UKC-695 ;
          etype:identification_UKC-36247 ?location_id ;
          etype:address_UKC-45004 ?address ;
          etype:municipality_UKC-45537 ?municipality .
    
  FILTER(?placed_id = ?location_id)
}
```

### CQ2: Luca also asks if there are any padel events during the weekend of the Festival dello Sport.
```sparql
PREFIX etype: <http://knowdive.disi.unitn.it/etype#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?givenName ?familyName ?event_name ?address ?municipality
WHERE {
  
  ?user rdf:type etype:User_UKC-53492 ;
    	etype:identification_UKC-36247 "1" ;
    	etype:given_name_UKC-33531 ?givenName ;
    	etype:family_name_UKC-33528 ?familyName .

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

SELECT DISTINCT ?givenName ?familyName ?event_name ?address ?municipality ?startDate ?endDate
WHERE {
    
  ?user rdf:type etype:User_UKC-53492 ;
    	etype:identification_UKC-36247 "1" ;
    	etype:given_name_UKC-33531 ?givenName ;
    	etype:family_name_UKC-33528 ?familyName .
    
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
         etype:name_UKC-2 ?event_name ;
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

SELECT DISTINCT ?givenName ?familyName ?name
WHERE {
    
    ?user rdf:type etype:User_UKC-53492 ;
    	etype:identification_UKC-36247 "2" ;
    	etype:given_name_UKC-33531 ?givenName ;
    	etype:family_name_UKC-33528 ?familyName .
    
    # Get Facilities
    ?facility rdf:type etype:Facility_UKC-17619 .
    
    # Retrieve sports associated with the facility
    ?have etype:have_UKC-103527 ?facility ;
          etype:identification_UKC-36247 ?have_sport_id .
    
    # Match sports details
    ?sport rdf:type etype:Sport_UKC-2593 ;
           etype:identification_UKC-36247 ?have_sport_id ;
           etype:name_UKC-2 ?name .
}

```

### CQ5: Spending the weekend with friends in Folgaria, Anna asks if there are any lighted volleyball or beach volleyball courts available throughout the day.
```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX etype: <http://knowdive.disi.unitn.it/etype#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?givenName ?familyName ?facility_name ?address
WHERE {
    
    ?user rdf:type etype:User_UKC-53492 ;
    	etype:identification_UKC-36247 "2" ;
    	etype:given_name_UKC-33531 ?givenName ;
    	etype:family_name_UKC-33528 ?familyName .
    
  # Match the facility
  ?facility rdf:type etype:Facility_UKC-17619 ;
    etype:identification_UKC-36247 ?sport_facility_id .
  
  # Make the name optional
  OPTIONAL {
    ?facility etype:name_UKC-2 ?facility_name .
  }

  # Extract the location of each facility
  ?placed etype:placed_UKC-85982 ?facility ;
    etype:identification_UKC-36247 ?placed_id .
  
  # Match the location
  ?location rdf:type etype:Location_UKC-695 ;
    etype:identification_UKC-36247 ?placed_id ;
    etype:municipality_UKC-45537 "Arco" .

  # Make the name optional
  OPTIONAL {
    ?location etype:address_UKC-45004 ?address .
  }
  
  # Extract the sport of each facility
  ?have etype:have_UKC-103527 ?facility;
     etype:identification_UKC-36247 ?have_sport_id .
  
  VALUES ?have_sport_id {"10" "65" "120" "133"}
    
  ?volleyball_field rdf:type etype:VolleyballField_KGE24-SportFacilities\&SportEvents-8004 ;
    etype:lit_UKC-75466 "True" .

  ?is etype:isEtype ?volleyball_field ;
    etype:identification_UKC-36247 ?facility_id .
    
  FILTER(?sport_facility_id = ?facility_id)
}
```

### CQ6: As a volleyball enthusiast, Anna would like to know if there will be any volleyball events during the summer holidays of 2024.
```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX etype: <http://knowdive.disi.unitn.it/etype#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?givenName ?familyName ?event_name ?startDate
WHERE {

    ?user rdf:type etype:User_UKC-53492 ;
    	etype:identification_UKC-36247 "2" ;
    	etype:given_name_UKC-33531 ?givenName ;
    	etype:family_name_UKC-33528 ?familyName .
    
    ?event rdf:type etype:Event_UKC-56 ;
         etype:identification_UKC-36247 ?event_id ;
         etype:name_UKC-2 ?event_name .
   	
    OPTIONAL {
        ?event etype:startDate_schema.org-startDate ?startDate .

          BIND(IF(STRLEN(?startDate) >= 8, 
                STRDT(SUBSTR(?startDate, 6, 2), xsd:integer), 
                false) AS ?summer_holiday)  
      }
   
    FILTER(?summer_holiday >= 5 && ?summer_holiday <= 9)
    
    ?based_on etype:basedOn_UKC-92536 ?event ;
            etype:identification_UKC-36247 ?based_on_sport_id .
	
    VALUES ?based_on_sport_id {"10" "65" "120" "133"}
}
```

### CQ7: Matteo also wants to know if there are any skiing events held in Stelvio National Park during the winter season.
```sparql
PREFIX etype: <http://knowdive.disi.unitn.it/etype#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?givenName ?familyName ?event_name ?address ?municipality ?winter_holiday
WHERE {
  
  ?user rdf:type etype:User_UKC-53492 ;
    	etype:identification_UKC-36247 "3" ;
    	etype:given_name_UKC-33531 ?givenName ;
    	etype:family_name_UKC-33528 ?familyName .
    
  # Match Event and Organization
  ?event rdf:type etype:Event_UKC-56 ;
         etype:identification_UKC-36247 ?event_id ;
         etype:name_UKC-2 ?event_name .
  
  OPTIONAL {
    ?event etype:startDate_schema.org-startDate ?startDate .

      BIND(IF(STRLEN(?startDate) >= 8, 
            SUBSTR(?startDate, 6, 2), 
            false) AS ?winter_holiday)  
  }
    
  # Match the Sport
  ?based_on etype:basedOn_UKC-92536 ?event ;
            etype:identification_UKC-36247 "79" .
    
  # Match Event's Location
  ?placed etype:placed_UKC-85982 ?event ;
          etype:identification_UKC-36247 ?placed_location_id .
  
  ?location rdf:type etype:Location_UKC-695 ;
            etype:identification_UKC-36247 ?location_id ;
            etype:address_UKC-45004 ?address ;
            etype:municipality_UKC-45537 "Stelvio" .
  
  FILTER(?placed_location_id = ?location_id)
}
```

### CQ8: Not finding what he’s looking for, Matteo asks if there are any sport events during his vacation in Trentino.
```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX etype: <http://knowdive.disi.unitn.it/etype#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?givenName ?familyName ?event_name ?startDate ?address ?municipality
WHERE {
  
    ?user rdf:type etype:User_UKC-53492 ;
    	etype:identification_UKC-36247 "3" ;
    	etype:given_name_UKC-33531 ?givenName ;
    	etype:family_name_UKC-33528 ?familyName .
    
  # Match Event and Organization
  ?event rdf:type etype:Event_UKC-56 ;
         etype:identification_UKC-36247 ?event_id ;
         etype:name_UKC-2 ?event_name .
  
  OPTIONAL {
    ?event etype:startDate_schema.org-startDate ?startDate .

      BIND(IF(STRLEN(?startDate) >= 8, 
            STRDT(SUBSTR(?startDate, 6, 2), xsd:integer), 
            false) AS ?winter_holiday)  
  }
  
  # Match the season
  FILTER(?winter_holiday && (xsd:integer(?winter_holiday) <= 2 || xsd:integer(?winter_holiday) >= 12))
  
  ?placed etype:placed_UKC-85982 ?event ;
          etype:identification_UKC-36247 ?location_id .
  
  ?location rdf:type etype:Location_UKC-695 ;
            etype:identification_UKC-36247 ?location_id ;
            etype:address_UKC-45004 ?address ;
            etype:municipality_UKC-45537 ?municipality .
}
ORDER BY ?startDate
```

### CQ9: A visitor asks Camilla about the events happening today, October 10, at the Festival dello Sport.
```sparql
PREFIX etype: <http://knowdive.disi.unitn.it/etype#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?givenName ?familyName ?event_name ?startDate ?address ?municipality
WHERE {
  
    ?user rdf:type etype:User_UKC-53492 ;
    	etype:identification_UKC-36247 "4" ;
    	etype:given_name_UKC-33531 ?givenName ;
    	etype:family_name_UKC-33528 ?familyName .
    
  # Match Event and Organization
  ?event rdf:type etype:Event_UKC-56 ;
         etype:identification_UKC-36247 ?event_id ;
         etype:name_UKC-2 ?event_name ;
       etype:startDate_schema.org-startDate ?startDate .
  
  FILTER(CONTAINS(?startDate, "2024-10-10"))

  ?organise etype:organise_UKC-104711 ?event ;
            etype:identification_UKC-36247 ?organise_organization_id .
  
  ?organization rdf:type etype:Organization_UKC-43416 ;
               etype:identification_UKC-36247 ?organization_id ;
               etype:name_UKC-2 "La Gazzetta dello Sport e Trentino Marketing" .
  
  FILTER(?organise_organization_id = ?organization_id)
    
  # Match Event's Location
  ?placed etype:placed_UKC-85982 ?event ;
          etype:identification_UKC-36247 ?location_id .
  
  ?location rdf:type etype:Location_UKC-695 ;
            etype:identification_UKC-36247 ?location_id ;
            etype:address_UKC-45004 ?address ;
            etype:municipality_UKC-45537 ?municipality .
}
ORDER BY ?startDate
```

### CQ10: While volunteering at the Festival dello Sport, Camilla becomes interested in tennis and wants to know if there are any tennis-related events.
```sparql
PREFIX etype: <http://knowdive.disi.unitn.it/etype#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?givenName ?familyName ?event_name ?address ?municipality
WHERE {
  
    ?user rdf:type etype:User_UKC-53492 ;
    	etype:identification_UKC-36247 "4" ;
    	etype:given_name_UKC-33531 ?givenName ;
    	etype:family_name_UKC-33528 ?familyName .
    
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
            etype:identification_UKC-36247 "97" .

  # Match Event's Location
  ?placed etype:placed_UKC-85982 ?event ;
          etype:identification_UKC-36247 ?location_id .
  
  ?location rdf:type etype:Location_UKC-695 ;
            etype:identification_UKC-36247 ?location_id ;
            etype:address_UKC-45004 ?address ;
            etype:municipality_UKC-45537 ?municipality .
}
```

### CQ11: Moreover, she wants to know if there are any tennis courts available when she returns to Molveno for the weekend. 
```sparql
PREFIX etype: <http://knowdive.disi.unitn.it/etype#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?givenName ?familyName ?name ?address
WHERE {
	
    ?user rdf:type etype:User_UKC-53492 ;
    	etype:identification_UKC-36247 "4" ;
    	etype:given_name_UKC-33531 ?givenName ;
    	etype:family_name_UKC-33528 ?familyName .
    
  ?facility rdf:type etype:Facility_UKC-17619 ;
         etype:identification_UKC-36247 ?facility_id ;
         etype:name_UKC-2 ?name .
    
  ?placed etype:placed_UKC-85982 ?facility ;
            etype:identification_UKC-36247 ?placed_location_id .
  
  ?location rdf:type etype:Location_UKC-695 ;
            etype:identification_UKC-36247 ?placed_location_id ;
        etype:address_UKC-45004 ?address ;
            etype:municipality_UKC-45537 "Bolzano" .
  
  ?have etype:have_UKC-103527 ?facility ;
            etype:identification_UKC-36247 "97" .
}
```