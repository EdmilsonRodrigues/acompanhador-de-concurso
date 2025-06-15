import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AboutComponent } from './components/about/about';
import { SignupComponent } from './components/signup/signup';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    CommonModule,
    AboutComponent,
    SignupComponent
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected title = 'Acompanhador de Concurso Público';
}
