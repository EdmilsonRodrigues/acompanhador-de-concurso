import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-signup',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './signup.html',
  styleUrl: './signup.scss'
})
export class SignupComponent {
  waitlistForm!: FormGroup;
  formSubmitted = false;
  successMessage = '';
  errorMessage = '';

  areasDeAtuacao = [
    // 'Professor',
    // 'Auxiliar Administrativo',
    // 'Engenheiro',
    // 'Saúde (Médico, Enfermeiro, etc.)',
    // 'Área Jurídica',
    // 'Tecnologia da Informação',
    // 'Segurança Pública',
    // 'Finanças e Contabilidade',
    // 'Meio Ambiente',
    // 'Outros'
  ];

  estadosDoBrasil = [
    // 'Acre (AC)', 'Alagoas (AL)', 'Amapá (AP)', 'Amazonas (AM)', 'Bahia (BA)',
    // 'Ceará (CE)', 'Distrito Federal (DF)', 'Espírito Santo (ES)', 'Goiás (GO)',
    // 'Maranhão (MA)', 'Mato Grosso (MT)', 'Mato Grosso do Sul (MS)', 'Minas Gerais (MG)',
    // 'Pará (PA)', 'Paraíba (PB)', 'Paraná (PR)', 'Pernambuco (PE)', 'Piauí (PI)',
    // 'Rio de Janeiro (RJ)', 'Rio Grande do Norte (RN)', 'Rio Grande do Sul (RS)',
    // 'Rondônia (RO)', 'Roraima (RR)', 'Santa Catarina (SC)', 'São Paulo (SP)',
    // 'Sergipe (SE)', 'Tocantins (TO)'
  ];

  constructor(private fb: FormBuilder, private router: Router, private authService: AuthService) { }

  ngOnInit(): void {
    this.waitlistForm = this.fb.group({
      fullName: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      confirmPassword: ['', Validators.required],
    });
  }

  /**
   * Getter for easy access to form controls.
   */
  get f() { return this.waitlistForm.controls; }

  /**
   * Handles the form submission.
   * Simulates sending data to a backend.
   */
  onSubmit(): void {
    this.formSubmitted = true;
    this.successMessage = '';
    this.errorMessage = '';

    if (this.waitlistForm.invalid) {
      this.errorMessage = 'Por favor, preencha todos os campos obrigatórios.';
      this.waitlistForm.markAllAsTouched();
      this.formSubmitted = false;
      return;
    }

    if (this.waitlistForm.value.password !== this.waitlistForm.value.confirmPassword) {
      this.errorMessage = 'As senhas devem ser iguais.';
      this.waitlistForm.markAllAsTouched();
      this.formSubmitted = false;
      return;
    }

    this.authService.signin({
      name: this.waitlistForm.value.fullName,
      email: this.waitlistForm.value.email,
      password: this.waitlistForm.value.password
    }).subscribe(() => {
      this.successMessage = 'Cadastro realizado com sucesso! Em breve entraremos em contato.';
      this.waitlistForm.reset();
      this.formSubmitted = false;
    });

    setTimeout(() => {
      this.router.navigate(['/']);
    }, 3000);
  }

  /**
   * Navigates back to the About page.
   */
  goBack(): void {
    this.router.navigate(['/']);
  }
}
