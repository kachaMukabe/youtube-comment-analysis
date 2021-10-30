
# Youtube comment analyzer

This api takes a youtube video url and returns a table of de-identified comments and their sentiment.
This shows the overall sentiment if a youtube video's sentiment is positive, negative or neutral.

## Demo

This application was built for the Pytorch 2021 hackathon and can be tested at [this]() site.
  
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DEVELOPER_KEY`


Get the youtube api key from your google developer console
## API Reference

#### Get comments sentiment

```http
  GET /api/v1/analyzeComments
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `video` | `string` | **Required**. Url of the video |

Takes a video url and returns the sentiment predictions of each comment
on the video.



  
## Lessons Learned


I continued to firm up my [htmx]() with flask to create a "SPA" like 
application.

## Roadmap

- Support for adding multiple video urls and queing to get video comment sentiments
- Adding support for multiple sites that have comments

  
## License

[MIT](https://choosealicense.com/licenses/mit/)

  