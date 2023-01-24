import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DetailService } from '../services/detail.service'
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css']
})

export class DetailComponent implements OnInit {

  id: string;
  detail: any;
  mapUrl: SafeResourceUrl;

  // center: google.maps.LatLngLiteral

  constructor(private route: ActivatedRoute, private detailService: DetailService, private sanitizer: DomSanitizer) {
    route.params.subscribe(val => {
      this.ngOnInit();
      // window.scrollTo(0, 0);
      let scrollToTop = window.setInterval(() => {
        let pos = window.pageYOffset;
        if (pos > 0) {
          window.scrollTo(0, pos - 20); // how far to scroll on each step
        } else {
          window.clearInterval(scrollToTop);
        }
      }, 16);
    });
  }

  imageDetails: Array<any> = [];

  ngOnInit(): void {
    this.id = this.route.snapshot.paramMap.get('id');
    this.loadDetail();
  }

  loadDetail() {
    this.detailService.getDetail(this.id).subscribe(data => {
      this.detail = data;
      console.log("detial");
      console.log(data);
      this.mapUrl = this.sanitizer.bypassSecurityTrustResourceUrl(this.detail.location_path);
      // this.center = {
      //   lat: this.detail.location.lat,
      //   lng: this.detail.location.lng
      // }
    });
  }
}
