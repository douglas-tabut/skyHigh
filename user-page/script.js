let navbar = document.querySelector('.header .navbar')

document.querySelector('#menu').onclick = () =>{
  navbar.classList.add('active');
}

document.querySelector('#close').onclick = () =>{
  navbar.classList.remove('active');
}


// mousemove home img

document.addEventListener('mousemove', move);
function move(e){
  this.querySelectorAll('.move').forEach(layer =>{
    const speed = layer.getAttribute('data-speed')

    const x = (window.innerWidth - e.pageX*speed)/120
    const y = (window.innerWidth - e.pageY*speed)/120

    layer.style.transform = `translateX(${x}px) translateY(${y}px)`

  })
}



gsap.from('.logo', {opacity: 0, duration: 1, delay: 2, y:10})
gsap.from('.navbar .nav_item', {opacity: 0, duration: 1, delay: 2.1, y:30, stagger: 0.2})

gsap.from('.title', {opacity: 0, duration: 1, delay: 1.6, y:30})
gsap.from('.description', {opacity: 0, duration: 1, delay: 1.8, y:30})
gsap.from('.btn', {opacity: 0, duration: 1, delay: 2.1, y:30})
gsap.from('.image', {opacity: 0, duration: 1, delay: 2.6, y:30})


// Function to handle user search
function handleSearch() {
  const searchInput = document.getElementById('searchInput').value;

  if (searchInput.trim() !== '') {
      displayLoadingIndicator(true);

      // Call the datascraper backend with the user's query
      makeBackendRequest(searchInput)
          .then(results => {
              displayLoadingIndicator(false);
              displaySearchResults(results);
          })
          .catch(error => {
              displayLoadingIndicator(false);
              displayError(error);
          });
  }
}

// Function to make a request to the datascraper backend
async function makeBackendRequest(query) {
  const response = await fetch(`/path/to/datascraper/backend?query=${query}`);

  if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
  }

  return response.json();
}

// Function to display loading indicator
function displayLoadingIndicator(show) {
  const loadingIndicator = document.getElementById('loadingIndicator');
  loadingIndicator.style.display = show ? 'block' : 'none';
}

// Function to update the UI with search results
function displaySearchResults(results) {
  const searchResultsContainer = document.getElementById('searchResults');
  // Implement the logic to update the UI based on the received results
  // This might involve creating or updating HTML elements dynamically
  // example, S create a list of search results.
  searchResultsContainer.innerHTML = `<ul>${results.map(result => `<li>${result}</li>`).join('')}</ul>`;
}

// Function to handle errors and display appropriate messages
function displayError(error) {
  // Implement the logic to display error messages on the UI
  const searchResultsContainer = document.getElementById('searchResults');
  searchResultsContainer.innerHTML = `<p>Error: ${error.message}</p>`;
}
