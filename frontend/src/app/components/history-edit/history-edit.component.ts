import { Component, inject, OnInit } from '@angular/core';
import { History } from '../../interfaces/history';
import { ApiService } from '../../services/api/api.service';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-history-edit',
  imports: [],
  templateUrl: './history-edit.component.html',
  styleUrl: './history-edit.component.scss'
})
export class HistoryEditComponent implements OnInit {
  history-item: History;

  constructor() { this.history-item = {}; }

  private apiService = inject(ApiService);

  ngOnInit(): void {
    this.getHistoryItem();
  }

  getHistoryItemData(): void {
    this.apiService.getHistoryItem().subscribe((res: any) => {
      this.history-item = res as History;
    })
  }
}
