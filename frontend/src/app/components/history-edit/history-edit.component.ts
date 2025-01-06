import { Component, inject, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { History } from '../../interfaces/history';
import { ApiService } from '../../services/api/api.service';
import { NgFor, CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { distinctUntilChanged } from 'rxjs/operators';
import { FormsModule } from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatDatepickerModule} from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import {provideNativeDateAdapter} from '@angular/material/core';



@Component({
  selector: 'app-history-edit',
  imports: [CommonModule, FormsModule, MatInputModule, MatFormFieldModule, MatDatepickerModule, MatNativeDateModule],
  templateUrl: './history-edit.component.html',
  styleUrl: './history-edit.component.scss',
  providers: [provideNativeDateAdapter()],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HistoryEditComponent implements OnInit {

  historyItem: History = {} as History;
  private apiService = inject(ApiService);
  private route = inject(ActivatedRoute); 

  constructor() {  }

  ngOnInit(): void {
    this.route.paramMap
      .pipe(distinctUntilChanged((prev, curr) => prev.get('id') === curr.get('id')))
      .subscribe((paramMap) => {
        const id = Number(paramMap.get('id'));
        if (id) {
          this.getHistoryItem(id);
        }
      });
  }

  // Pobieranie parametru `id` i wywołanie API
  loadHistoryItem(): void {
    const id = Number(this.route.snapshot.paramMap.get('id')); // Pobiera parametr `id`
    if (id) {
      this.getHistoryItem(id);
    }
  }

  // Wywołanie metody serwisu z przekazanym `id`
  getHistoryItem(id: number): void {
    this.apiService.getHistoryItem(id).subscribe((res: History) => {
      this.historyItem = res;
    });
  }

  saveHistoryItem(): void {
    if (this.historyItem.id) {
      // Aktualizacja istniejącego wpisu
      this.apiService.updateHistoryItem(this.historyItem.id, this.historyItem)
        .subscribe({
          next: (res) => {
            console.log('Zaktualizowano:', res);
            alert('Wpis zaktualizowany!');
          },
          error: (err) => {
            console.error('Błąd aktualizacji:', err);
            alert('Wystąpił błąd podczas aktualizacji.');
          }
        });
    } else {
      // Dodanie nowego wpisu
      this.apiService.createHistoryItem(this.historyItem)
        .subscribe({
          next: (res) => {
            console.log('Dodano nowy wpis:', res);
            alert('Nowy wpis dodany!');
          },
          error: (err) => {
            console.error('Błąd dodawania wpisu:', err);
            alert('Wystąpił błąd podczas dodawania.');
          }
        });
    }
  }
}
