import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-pagination',
  standalone: true,
  templateUrl: './pagination.html',
  styleUrls: ['./pagination.css']
})
export class PaginationComponent {
  @Input() totalRecords: number = 0;
  @Input() rows: number = 10;
  @Input() currentPage: number = 1;

  @Output() pageChanged = new EventEmitter<number>();

  get totalPages() {
    return Math.ceil(this.totalRecords / this.rows);
  }

  changePage(page: number) {
    if (page < 1 || page > this.totalPages) return;
    this.currentPage = page;
    this.pageChanged.emit(this.currentPage);
  }
}
