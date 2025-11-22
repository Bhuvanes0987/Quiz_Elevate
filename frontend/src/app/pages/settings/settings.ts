import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-settings',
  standalone: true,
  templateUrl: './settings.html',
  styleUrls: ['./settings.css'],
  imports: [
    CommonModule,
    RouterLink,
    RouterLinkActive,
    RouterOutlet
  ]
})
export class settingscomponent {

  selectedMenu: string = 'user-subjects';

  selectMenu(menu: string) {
    this.selectedMenu = menu;
  }
}
