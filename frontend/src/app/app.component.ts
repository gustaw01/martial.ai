import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { HistoryComponent } from './components/history/history.component';
import { HttpClient } from '@angular/common/http';
import { environment } from './environments/environment.development';

@Component({
    selector: 'app-root',
    imports: [RouterOutlet, HeaderComponent, FooterComponent, HistoryComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'frontend';

  // constructor() {
  //   this.http = inject(HttpClient);
  // }

  // private http: HttpClient;

  // ngOnInit() {
  //   this.http.get(`${environment.apiUrl}/history`).subscribe((data) => {
  //     console.log(data);
  //   });
  // }
}
