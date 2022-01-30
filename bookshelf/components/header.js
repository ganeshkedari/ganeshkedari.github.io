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
  
        
      </header>
        `
      }
  }

  
  customElements.define('header-component', Header);
