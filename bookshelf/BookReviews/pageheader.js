class Header extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML = `
        <header class="header">
        <!-- Top bar -->
        <div class="py-2 bg-dark text-white">
          <div class="container py-1">
            <div class="row align-items-center">
              <div class="col-lg-4">
                <ul class="list-inline mb-0 text-small">
                  <li class="list-inline-item"><a href="https://ganeshkedari.github.io/">Atelier of a G∑∑K</a></li>
                  <!-- <li class="list-inline-item">|</li>
                    <li class="list-inline-item"><a class="reset-anchor" href="#">Sitemap</a></li> -->
                </ul>
              </div>
              <div class="col-lg-4 d-none d-lg-block text-center">
    
              </div>
              <div class="col-lg-4 d-none d-lg-block text-right">
    
              </div>
            </div>
          </div>
        </div>
        <!-- Navbar 1 -->
        
        <!-- Navbar 2 -->
        <nav class="navbar navbar-expand-lg navbar-light border-gray py-2 bg-light">
          <div class="container">
            <button class="navbar-toggler navbar-toggler-right mx-auto border-0" type="button" data-toggle="collapse"
              data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
              aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>
            <div class="collapse navbar-collapse text-center" id="navbarSupportedContent">
              <ul class="navbar-nav mx-auto">
              <li class="nav-item px-1">
              <a class="nav-link" href="../index.html">Home</a>
            </li>
                <li class="nav-item px-1">
                  <a class="nav-link" href="#">Fiction</a>
                </li>
                <li class="nav-item px-1">
                  <a class="nav-link" href="#">History</a>
                </li>
                <li class="nav-item px-1">
                  <a class="nav-link" href="#">Mythology</a>
                </li>
                <li class="nav-item px-1">
                  <a class="nav-link" href="#">Naval</a>
                </li>
    
                <li class="nav-item px-1">
                  <a class="nav-link" href="#">Sci-Fi</a>
                </li>
                <li class="nav-item px-1">
                  <a class="nav-link" href="#">Self Help</a>
                </li>
                <li class="nav-item px-1">
                  <a class="nav-link" href="#">Marathi</a>
                </li>
                
    
              </ul>
            </div>
          </div>
        </nav>
  
        
      </header>
        `;
    }
}


customElements.define('header-component', Header);