import { Injectable } from "@angular/core";
import {
  HttpClient,
  HttpRequest,
  HttpEventType,
  HttpEvent
} from "@angular/common/http";
import { map, tap, last } from "rxjs/operators";
import { BehaviorSubject } from "rxjs";

@Injectable({
  providedIn: "root"
})
export class UploaderService {
  public progressSource = new BehaviorSubject<number>(0);

  constructor(private http: HttpClient) {}

  upload(file: File) {
    const uploadUrl = "http://127.0.0.1:5000/upload"

    let formData = new FormData();
    formData.append("avatar", file);

    const req = new HttpRequest(
      "POST",
      uploadUrl,
      formData,
      {
        reportProgress: true
      }
    );

    return this.http.post<Array<any>>(uploadUrl,formData)
    .pipe(
      // map(event => this.getEventMessage(event, file)),
      // tap((envelope: any) => this.processProgress(envelope)),
      last()
    );
  }

  processProgress(envelope: any): void {
    if (typeof envelope === "number") {
      this.progressSource.next(envelope);
    }
  }

  private getEventMessage(event: HttpEvent<any>, file: File) {
    switch (event.type) {
      case HttpEventType.Sent:
        return `Uploading file "${file.name}" of size ${file.size}.`;
      case HttpEventType.UploadProgress:
        return Math.round((100 * event.loaded) / event.total);
      case HttpEventType.Response:
        return `File "${file.name}" was completely uploaded!`;
      default:
        return `File "${file.name}" surprising upload event: ${event.type}.`;
    }
  }
}