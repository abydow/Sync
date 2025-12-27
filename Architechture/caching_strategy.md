## multi-layer caching prevents database queries from becoming bottleneck:

```ascii
╭⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯╮ ╭⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯╮ ╭⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯╮
┊ Application Memory (L1) ┊→┊ Redis (L2) ┊→┊ PostgreSQL (L3) ┊
╰⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯╯ ╰⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯╯ ╰⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯╯
```

- Its the basic plan and little fun ascii art cause without fun there is no difference between a personal and a commercial project 😆
