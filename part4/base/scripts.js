

async function loginUser(email, password) {

   const response = await fetch('http://localhost:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password }),
      mode: 'cors'
  });
 // Handle the response
  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}


function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const addReview = document.getElementById('add-review');

  if (loginLink) {
    if (!token) {
      loginLink.style.display = 'block';
    } else {
      loginLink.style.display = 'none';
    }
  }

  if (addReview) {
    if (!token) {
      addReview.style.display = 'none';
    } else {
      addReview.style.display = 'block';
    }
  }

  return token;
}


function getCookie(name) {
  // Function to get a cookie value by its name
  const cookies = document.cookie.split(';')
  const foundCookie = cookies.find(
    (cookie) => cookie.split('=')[0].trim() === name
  )
  if (foundCookie) {
    const cookieValue = foundCookie.split('=')[1]
    return cookieValue;
  }
  return '';
}


async function fetchPlaces(token) {
  const headers = {
    'Content-Type': 'application/json'
  };

  // if (token) {
  //   headers['Authorization'] = `Bearer ${token}`;
  // }

  const response = await fetch('http://localhost:5000/api/v1/places/', {
    method: 'GET',
    headers: headers
  });

  if (response.ok) {
    const data = await response.json();
    console.log(data);
    return data;
  } else {
    console.error('Error fetching places: ' + response.statusText);
    return [];
  }
}

function displayPlaces(places, filter_price) {
  const placesList = document.getElementById('places-list')
  placesList.innerHTML = '';
  if (!places || places.length === 0){
    placesList.textContent = 'There are 0 locations registered.';
    return;
  }

  const placeCard = document.createElement('div');
  placeCard.classList.add('place-card');

  places.forEach(place => {
    if (filter_price === 0 || filter_price <= place.price) {
      const placeData = document.createElement('ul');
      placeData.classList.add('place-data');

      // Title
      const li_title = document.createElement('li');
      const h2_title = document.createElement('h2');
      h2_title.textContent = place.title;

      // price
      const li_price = document.createElement('li');
      li_price.textContent = `Price per night: $${place.price}`;

      // button
      const li_button = document.createElement('li');
      li_button.classList.add('details-button');
      const btn_button = document.createElement('button');
      btn_button.textContent = 'View Details';

      btn_button.addEventListener('click', () => {
        // Redirect to the details page with the place id
        window.location.href = `place.html?id=${place.id}`;
      });

      li_title.appendChild(h2_title);
      placeData.appendChild(li_title);
      placeData.appendChild(li_price);
      li_button.appendChild(btn_button);
      placeData.appendChild(li_button);
      placeCard.appendChild(placeData);
    }
  });

  placesList.appendChild(placeCard);

}


function getPlaceIdFromURL() {
  const url = new URL(window.location.href);
  const place_id = url.searchParams.get('id');
  return place_id;
}


async function fetchPlaceDetails(token, placeId) {
  const headers = {
    'Content-Type': 'application/json'
  };

  // if (token) {
  //   headers['Authorization'] = `Bearer ${token}`;
  // }

  const response = await fetch('http://localhost:5000/api/v1/places/'+placeId, {
    method: 'GET',
    headers: headers
  });

  if (response.ok) {
    const data = await response.json();
    console.log(data);
    return data;
  } else {
    console.error('Error fetching place details: ' + response.statusText);
    return [];
  }
}


async function fetchUserDetails(userId) {
  const headers = {
    'Content-Type': 'application/json'
  };

  // if (token) {
  //   headers['Authorization'] = `Bearer ${token}`;
  // }

  const response = await fetch('http://localhost:5000/api/v1/users/'+ userId, {
    method: 'GET',
    headers: headers
  });

  if (response.ok) {
    const data = await response.json();
    console.log(data);
    return data;
  } else {
    console.error('Error fetching place details: ' + response.statusText);
    return [];
  }
}


function displayPlaceDetails(place) {
  // Clear the current content of the place details section
  // Create elements to display the place details (name, description, price, amenities and reviews)
  // Append the created elements to the place details section

  // place info
  const placeDtails = document.getElementById('place-details')
  placeDtails.innerHTML = '';

  const placeTitle = document.createElement('p');
  placeTitle.textContent = place.title;

  const div_place = document.createElement('div');
  const ul_place = document.createElement('ul');
  ul_place.classList.add('place-info');

  // owner's name
  const li_owner = document.createElement('li');
  li_owner.innerHTML = `<span>Host:</span> ${place.owner.first_name} ${place.owner.last_name}`;

  // price
  const li_price = document.createElement('li');
  li_price.innerHTML = `<span>Price per night:</span> $${place.price}`;

  // description
  const li_description = document.createElement('li');
  li_description.innerHTML = `<span>Description:</span> ${place.description}`;

  // amenities
  const li_amenities = document.createElement('li');
  li_amenities.innerHTML = `<span>Amenities:</span> `;

  if (place.amenities.length === 0) {
    li_amenities.innerHTML += 'no amenity infomation';
  } else {
    let cnt = 1;
    place.amenities.forEach(amenity => {
      li_amenities.innerHTML += amenity.name;

      if (cnt !== place.amenities.length) {
        li_amenities.innerHTML += ', ';
      }

      cnt += 1;
    });
  }

  ul_place.appendChild(li_owner);
  ul_place.appendChild(li_price);
  ul_place.appendChild(li_description);
  ul_place.appendChild(li_amenities);
  div_place.appendChild(ul_place);

  placeDtails.appendChild(placeTitle);
  placeDtails.appendChild(div_place);


  // place review
  const placeReviews = document.getElementById('reviews')
  placeReviews.innerHTML = '';

  const h2_review = document.createElement('h2');
  h2_review.classList.add('review-h2');
  h2_review.textContent = 'Reviews';
  placeReviews.appendChild(h2_review);

  if (place.reviews.length !== 0) {
    place.reviews.forEach((review) => {
      const div_review = document.createElement('div');
      const ul_review = document.createElement('ul');
      ul_review.classList.add('review-card');

      // user's name
      const li_user = document.createElement('li');

      // get user infomation
      fetchUserDetails(review.user_id)
        .then(user_info => {
              li_user.innerHTML = `<span>${user_info.first_name} ${user_info.last_name}:</span>`});

      // review text
      const li_text = document.createElement('li');
      li_text.textContent = review.text;

      // rating
      const li_rating = document.createElement('li');
      li_rating.textContent = 'Rating: ' + review.rating;

      ul_review.appendChild(li_user);
      ul_review.appendChild(li_text);
      ul_review.appendChild(li_rating);
      div_review.appendChild(ul_review);

      placeReviews.appendChild(div_review);
    });
  } else {
    const p_review = document.createElement('p');
    p_review.classList.add('review-card');
    p_review.textContent = 'No reviews';
    placeReviews.appendChild(p_review);
  }
}


async function submitReview(token, placeId, reviewText, reviewRating) {

  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  };

headers['Authorization'] = `Bearer ${token}`;

  const response = await fetch('http://localhost:5000/api/v1/reviews/', {
    method: 'POST',
    headers: headers,
    body: JSON.stringify({ 
      place_id: placeId,
      text: reviewText,
      rating: reviewRating
    })

  });
// Handle the response
  if (response.ok) {
    //window.location.href = 'place.html';
    alert('Review added successfully');

    //clear form
    const form = document.getElementById('review-form');
    form.reset();
  } else {
      const errorData = await response.json();
      console.error('Error:', errorData); 
      if(errorData.message){ 
        alert('Failed to submit review: ' +errorData.message);
      } else {
        alert('Failed to submit review: ' +errorData.msg);
      }
      // alert('Failed to submit review: ' + response.statusText);
    }
}


//---------------------------------------------------------------------//


document.addEventListener('DOMContentLoaded', () => {


  const includeHeader = new XMLHttpRequest();
  includeHeader.open("GET", "header.html", true);
  includeHeader.onreadystatechange = function () {
    if (includeHeader.readyState === 4 && includeHeader.status === 200) {
      const headerHTML = includeHeader.responseText;
      const header = document.querySelector("header");
      header.insertAdjacentHTML("afterbegin", headerHTML);
    }
  };
  includeHeader.send();

  const includefooter = new XMLHttpRequest();
  includefooter.open("GET", "footer.html", true);
  includefooter.onreadystatechange = function () {
    if (includefooter.readyState === 4 && includefooter.status === 200) {
      const footerHTML = includefooter.responseText;
      const footer = document.querySelector("footer");
      footer.insertAdjacentHTML("afterbegin", footerHTML);
    }
  };
  includefooter.send();

  const includeaddReview = new XMLHttpRequest();
  includeaddReview.open("GET", "add_review.html", true);
  includeaddReview.onreadystatechange = function () {
    if (includeaddReview.readyState === 4 && includeaddReview.status === 200) {
      const addReviewHTML = includeaddReview.responseText;
      const addReview = document.querySelector("#add-review");
      addReview.insertAdjacentHTML("afterbegin", addReviewHTML);
    }
  };
  includeaddReview.send();



  const token = checkAuthentication();
  let filter_price = 0;

  const loginForm = document.getElementById('login-form');

  //login.html
  if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
          event.preventDefault();

          // Your code to handle form submission
          const target = event.target;

          await loginUser(target.email.value, target.password.value);
      });
  }


  // index.html
  const priceFilter = document.getElementById('price-filter');

  if (priceFilter) {

    // Populate places list
    fetchPlaces(token)
      .then(places => {displayPlaces(places, filter_price)});

    priceFilter.addEventListener('change', (event) => {
      // Get the selected price value
      // Iterate over the places and show/hide them based on the selected price

      filter_price = event.target.value;

      fetchPlaces(token)
        .then(places => {displayPlaces(places, Number(filter_price))});
    });
  }


  // place.html
  const placeDetails = document.getElementById('place-details');
  if (placeDetails) {
    const placeId = getPlaceIdFromURL();
    fetchPlaceDetails(token, placeId)
      .then(place => {displayPlaceDetails(place)});
  }

  // place.html, add_review.html
  const addReview = document.getElementById('add-review');
  if (addReview) {
    addReview.addEventListener('submit', async (event) => {
        event.preventDefault();

        const placeId = getPlaceIdFromURL();
        const target = event.target;

        const reviewText = document.getElementById('review-text').value;
        const reviewRating = document.getElementById('review-filter').value;

        await submitReview(token, placeId, reviewText, Number(reviewRating));

    });
  }


});