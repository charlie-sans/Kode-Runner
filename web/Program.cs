using Microsoft.AspNetCore.Mvc.Razor;
using Microsoft.Extensions.Hosting;
var builder = WebApplication.CreateBuilder(args);

 void ConfigureServices(IServiceCollection services)
{
    services.AddControllersWithViews()
            .AddRazorRuntimeCompilation();
}
// Add services to the container.
builder.Services.AddRazorPages();

builder.Services.Configure<RazorViewEngineOptions>(options =>
{

    options.AreaViewLocationFormats.Add("/Areas/{2}/Views/{1}/{0}.cshtml");
    options.AreaViewLocationFormats.Add("/Areas/{2}/Views/Shared/{0}.cshtml");
    options.AreaViewLocationFormats.Add("/Views/Shared/{0}.cshtml");
});
var app = builder.Build();
// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

app.UseEndpoints(endpoints =>
{
    endpoints.MapControllerRoute(
      name: "areas",
      pattern: "{area:exists}/{controller=Home}/{action=Index}/{id?}"
    );
});


app.MapRazorPages();

app.Run();