import { Component, inject, OnInit } from '@angular/core';
import { History } from '../../interfaces/history';
import { ApiService } from '../../services/api/api.service';
import { NgFor } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [NgFor, RouterLink],
  templateUrl: './history.component.html',
  styleUrl: './history.component.scss'
})
export class HistoryComponent implements OnInit {

  history: History[];

  constructor() { this.history = []; }

  private apiService = inject(ApiService);

  ngOnInit(): void {
      this.getHistoryData();
  }

  getHistoryData(): void {
    this.apiService.getHistoryList().subscribe((res: any) => {
      this.history = res as History[];
    })
  }
  
}
