The Dodge Oracle 🔮
Um script simples em Python que criei para ver a winrate (taxa de vitória) geral do meu time na tela de seleção de campeões do League of Legends.

A ideia do projeto é bem direta: automatizar aquela pesquisa chata de ter que digitar o nome de todo mundo no site para saber se o time está numa sequência de derrotas ou se vale a pena dar "dodge" (quitar da partida).

Como funciona
O script roda no terminal em segundo plano.

Ele lê os arquivos do Client do LoL (através do lockfile) para se conectar à API local do jogo e descobrir quem acabou de entrar no meu lobby.

Com os nicks em mãos, ele faz um Web Scraping rápido no site LeagueOfGraphs.

O resultado aparece no terminal: o nome do jogador, o campeão que ele clicou e a winrate geral da conta dele.
