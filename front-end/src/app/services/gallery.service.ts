import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class GalleryService {

  constructor(private httpClient: HttpClient) { }

  getGallery() {
    const uploadUrl = "http://127.0.0.1:5000"
    return this.httpClient.get<Array<any>>(`${uploadUrl}/gallery`);
  }
}
