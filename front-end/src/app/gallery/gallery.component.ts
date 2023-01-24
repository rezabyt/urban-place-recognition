import { Component, OnInit } from '@angular/core';
import { GalleryService } from '../services/gallery.service'


@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.css']
})
export class GalleryComponent implements OnInit {
  galleryImages: Array<any> = [];

  constructor(private galleryService: GalleryService) { }

  ngOnInit(): void {
    this.loadGallery();
  }

  loadGallery() {
    this.galleryService.getGallery().subscribe(data => {
      this.galleryImages = data;
      console.log("detial");
      console.log(data);
    });
  }
}
