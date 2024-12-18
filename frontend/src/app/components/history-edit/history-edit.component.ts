import { Component, inject, OnInit } from '@angular/core';
import { History } from '../../interfaces/history';
import { ApiService } from '../../services/api/api.service';
import { NgFor, CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-history-edit',
  imports: [CommonModule],
  templateUrl: './history-edit.component.html',
  styleUrl: './history-edit.component.scss'
})
export class HistoryEditComponent implements OnInit {

  historyItem: History = {} as History;
  private apiService = inject(ApiService);
  private route = inject(ActivatedRoute); 

  constructor() {  }

  ngOnInit(): void {
    this.loadHistoryItem();
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
}
