#[macro_use] extern crate rocket;
use rocket::fs::FileServer;
// index route handler
#[get("/")]
fn index() -> rocket::response::content::RawHtml<&'static str> {
  rocket::response::content::RawHtml("./index.html")
}

// launch rocket server
#[launch]
fn rocket() -> _ {
  let static_files = FileServer::from("./");
    rocket::build().mount("/", static_files)
}
