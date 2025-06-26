based on the description we can understand its an airport in russia and its so old that it doesn't have an internet access knowing these 2 factors we can go to https://overpass-turbo.eu/ then using this query we will get around 7 or 8 airports in russia going through them we will find one that matches the picture here its openstreetmap tags : 
-----
Way 377423382 ✏
Tags 6
addr:city = Манилы
addr:postcode = 688863
aeroway = aerodrome
internet_access = no
name = Аэровокзал с. Манилы
operator = ФКП "Аэропорты Камчатки"
-----
we can see one of the tags mention its operator doing a simple google we can find their website and then we go to the contact page and will find their number like this +7 (415-2) 308-308 we make sure to remove the spaces and brackets from it to match the flag format:

Query:
```
[out:json][timeout:25];
// fetch area “russia” to search in
{{geocodeArea:russia}}->.searchArea;
// gather results
nwr["aeroway"="aerodrome"]["internet_access"="no"](area.searchArea);
// print results
out geom;
```
