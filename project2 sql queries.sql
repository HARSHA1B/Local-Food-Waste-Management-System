select * from providers;
select * from recievers;
select * from food_listing;
select * from claim;

--Task1--number of food providers and receivers in each city..
select city,
sum(case when role='provider' then 1 else 0 end)as total_providers,
sum(case when role='receiver' then 1 else 0 end)as total_receivers
from
(select city,'provider' as role from providers
union all
select city,'receiver' as role from recievers)
as combined_data
group by city order by city;

--Task2--which food provider(restaurant,grocery store etc) contributes the most food?..
select provider_type, count(provider_type) as total_contribute
from food_listing
group by provider_type;

--Task3--what is the contact information of food providers in a specific city?..
select city,provider_name, contact,address
from providers
where city = 'New Jessica';

--Task4--which  receivers have claimed the most food?..
select claim.receiver_id, recievers.type, count(claim.receiver_id) as total_count
from claim join recievers on claim.receiver_id= recievers.receiver_id
group by claim.receiver_id,recievers.type
order by total_count desc limit 5;

--Task5--what is the total quantity of food avaialable from all the providers?...
select provider_type,sum(quantity) as total_available_food
from food_listing
group by provider_type;

--Task6--which city has highest number of food listing?...
select location, count(meal_type) as highest_food_listing
from food_listing
group by location
order by highest_food_listing desc limit 1;

--Task7--what are the most commonly available food types?..
select food_type, count(food_type) as commonly_available
from food_listing
group by food_type;

--Task8--how many food claims have made for each food item?...
select food_listing.food_name, count(claim.claim_id) as total_claims
from food_listing join claim on claim.food_id=food_listing.food_id
group by food_listing.food_name;

--Task9--which provider has highest number of successfull food claims?...
select food_listing.provider_type,count(claim.status) as no_of_successfull_claims
from food_listing join claim on food_listing.food_id=claim.food_id
group by food_listing.provider_type,claim.status
having claim.status='Completed';

--Task10--what percentage of food claims are completed vs pending vs cancelled?..
select status,count(status) as total_counts, round((count(status)*100)/sum(count(status))over(), 2 )as percentage
from claim
group by status;

--Task11--what is the average quantity of food claimed per receiver?..
select claim.receiver_id, round(avg(food_listing.quantity),0) as avg_quantity
from claim join food_listing on claim.food_id= food_listing.food_id
group by claim.receiver_id;

--Task12--which meal type(breakfast,lunch,dinner,snacks) is claimed the most?..
select food_listing.meal_type,count(claim.claim_id) as total_claimed
from food_listing join claim on food_listing.food_id=claim.food_id
group by food_listing.meal_type
order by total_claimed desc;

--Task13--what is the total quantity of food donated by each provider?..
select provider_type, sum(quantity) as total_quantity
from food_listing
group by provider_type;


--Task14--what are the highest demand food locations based on food claims?.. 
select food_listing.location, count(claim.claim_id) as total_claims
from food_listing join claim on food_listing.food_id=claim.food_id
group by food_listing.location
order by total_claims desc; 

--Task15--The most frequent food providers and their contributions..
select provider_id,provider_type,count(food_id) as total_donation ,sum(quantity) as total_contribution
from food_listing
group by provider_id,provider_type
order by total_contribution desc ,total_donation desc limit 10; 