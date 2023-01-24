import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class DetailService {
  
  constructor(private httpClient: HttpClient) { }

  getDetail(id: string) {
    const uploadUrl = "http://127.0.0.1:5000"
    return this.httpClient.get(`${uploadUrl}/detail/${id}`);
  }
}
