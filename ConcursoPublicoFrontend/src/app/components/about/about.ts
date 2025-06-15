import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-about',
  imports: [CommonModule],
  templateUrl: './about.html',
  styleUrl: './about.scss'
})
export class AboutComponent {
  constructor(private router: Router) {}

  /**
   * Navigates to the signup page.
   * @remarks This function is called when the "Entrar na Lista de Espera" button is clicked.
   */
  goToSignup(): void {
    this.router.navigate(['/signup']);
  }

}
