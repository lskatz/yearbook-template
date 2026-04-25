---
layout: print
title: "Full Yearbook — Print Edition"
permalink: /print/
---
{%- comment -%}
  =============================================================================
  print.md — the full-yearbook print / PDF page (/print/)
  =============================================================================
  This page renders every section of the yearbook in one long, continuous
  document so the browser can paginate it into a print-ready PDF.

  Order:
    1. Cover page
    2. Table of contents
    3. Classes  (one article per class, each starting on a new page)
    4. Clubs    (one article per club)
    5. Sports   (one article per team)
    6. Staff    (all staff/teachers together)
    7. Photo pages
    8. Back cover
    9. Printing instructions (screen-only)
  =============================================================================
{%- endcomment -%}

{%- comment -%} ═══ 1. COVER ═══ {%- endcomment -%}
<section class="print-cover print-page-break">
  <div class="print-cover__accent-bar"></div>
  <div class="print-cover__body">
    <p class="print-cover__eyebrow">{{ site.school_year }}</p>
    <h1 class="print-cover__title">{{ site.title }}</h1>
    <div class="print-cover__rule"></div>
    <p class="print-cover__mascot">Home of {{ site.mascot }}</p>
    <p class="print-cover__label">Yearbook</p>
  </div>
  <div class="print-cover__accent-bar"></div>
</section>

{%- comment -%} ═══ 2. TABLE OF CONTENTS ═══ {%- endcomment -%}
{%- assign classes_sorted = site.classes | sort: "grade_sort" -%}
<section class="print-toc print-page-break">
  <header class="print-toc__header">
    <h2 class="print-toc__title">Contents</h2>
  </header>
  <ol class="print-toc__list">
    {%- for c in classes_sorted %}
    <li class="print-toc__item">
      <span class="print-toc__label">
        {%- if c.grade == "PK" -%}Pre-K
        {%- elsif c.grade == 0 or c.grade == "K" -%}Kinder.
        {%- else -%}Grade {{ c.grade }}
        {%- endif -%}
      </span>
      <span class="print-toc__name">{{ c.title }}</span>
    </li>
    {%- endfor %}
    {%- for club in site.clubs %}
    <li class="print-toc__item">
      <span class="print-toc__label">{{ site.labels.eyebrow_club }}</span>
      <span class="print-toc__name">{{ club.title }}</span>
    </li>
    {%- endfor %}
    {%- for team in site.sports %}
    <li class="print-toc__item">
      <span class="print-toc__label">{{ site.labels.eyebrow_sport }}</span>
      <span class="print-toc__name">{{ team.title }}</span>
    </li>
    {%- endfor %}
    <li class="print-toc__item">
      <span class="print-toc__label">{{ site.labels.eyebrow_staff }}</span>
      <span class="print-toc__name">Faculty &amp; Staff</span>
    </li>
    {%- if site.photos and site.photos.size > 0 %}
    {%- for pp in site.photos %}
    <li class="print-toc__item">
      <span class="print-toc__label">Photos</span>
      <span class="print-toc__name">{{ pp.title }}</span>
    </li>
    {%- endfor %}
    {%- endif %}
    {%- if site.data.superlatives and site.data.superlatives.size > 0 %}
    <li class="print-toc__item">
      <span class="print-toc__label">{{ site.labels.eyebrow_superlatives | default: "Superlatives" }}</span>
      <span class="print-toc__name">Class Superlatives</span>
    </li>
    {%- endif %}
    {%- if site.data.year_in_review %}
    <li class="print-toc__item">
      <span class="print-toc__label">{{ site.labels.eyebrow_yir | default: "Year in Review" }}</span>
      <span class="print-toc__name">{{ site.data.year_in_review.school_year }} in Review</span>
    </li>
    {%- endif %}
    {%- if site.data.favorites and site.data.favorites.size > 0 %}
    <li class="print-toc__item">
      <span class="print-toc__label">{{ site.labels.eyebrow_favorites | default: "Favorites" }}</span>
      <span class="print-toc__name">Student Favorites</span>
    </li>
    {%- endif %}
    {%- if site.data.dedications and site.data.dedications.size > 0 %}
    <li class="print-toc__item">
      <span class="print-toc__label">{{ site.labels.eyebrow_dedications | default: "Dedications &amp; Ads" }}</span>
      <span class="print-toc__name">Dedications &amp; Ads</span>
    </li>
    {%- endif %}
    <li class="print-toc__item">
      <span class="print-toc__label">{{ site.labels.eyebrow_autographs | default: "Autographs" }}</span>
      <span class="print-toc__name">Autograph Pages</span>
    </li>
    <li class="print-toc__item">
      <span class="print-toc__label">Index</span>
      <span class="print-toc__name">Index</span>
    </li>
  </ol>
</section>

{%- comment -%} ═══ 3. CLASSES ═══ {%- endcomment -%}
{%- for c in classes_sorted %}
{%- assign class_slug = c.url | remove_first: '/classes/' | remove: '/' -%}
<article class="print-section print-page-break" id="print-section-class-{{ class_slug }}">

  <header class="print-section__header">
    <p class="print-section__eyebrow">
      {%- if c.grade == "PK" -%}Pre-K
      {%- elsif c.grade == 0 or c.grade == "K" -%}Kindergarten
      {%- else -%}Grade {{ c.grade }}
      {%- endif -%}
    </p>
    <h2 class="print-section__title">{{ c.title }}</h2>
    {%- if c.room %}<p class="print-section__meta">{{ c.room }}</p>{%- endif %}
  </header>

  {%- comment -%} Class thumbnail(s) {%- endcomment -%}
  {%- if c.thumbnails and c.thumbnails.size > 0 %}
    {%- for thumb_src in c.thumbnails %}
    <div class="print-thumbnail">
      <img src="{{ thumb_src | relative_url }}" alt="{{ c.title }} class photo" class="print-thumbnail__img">
    </div>
    {%- endfor %}
  {%- else %}
    {%- assign thumb_src = c.thumbnail | default: site.class_thumbnail_default -%}
    {%- if thumb_src and thumb_src != "" %}
    <div class="print-thumbnail">
      <img src="{{ thumb_src | relative_url }}" alt="{{ c.title }} class photo" class="print-thumbnail__img">
    </div>
    {%- endif %}
  {%- endif %}

  {%- if c.teachers and c.teachers.size > 0 %}
  <section class="roster">
    <h3 class="roster__heading">
      {%- if c.teachers.size > 1 -%}{{ site.labels.teachers_many }}{%- else -%}{{ site.labels.teachers_one }}{%- endif -%}
    </h3>
    <div class="roster__grid roster__grid--lg">
      {%- for tid in c.teachers %}
        {% include person-card-print.html id=tid size="lg" %}
      {%- endfor %}
    </div>
  </section>
  {%- endif %}

  {%- if c.students and c.students.size > 0 %}
  <section class="roster">
    <h3 class="roster__heading">{{ site.labels.students }}</h3>
    <div class="roster__grid">
      {%- for sid in c.students %}
        {% include person-card-print.html id=sid %}
      {%- endfor %}
    </div>
  </section>
  {%- endif %}

</article>
{%- endfor %}

{%- comment -%} ═══ 4. CLUBS ═══ {%- endcomment -%}
{%- for club in site.clubs %}
{%- assign club_slug = club.url | remove_first: '/clubs/' | remove: '/' -%}
<article class="print-section print-page-break" id="print-section-club-{{ club_slug }}">

  <header class="print-section__header">
    <p class="print-section__eyebrow">{{ site.labels.eyebrow_club }}</p>
    <h2 class="print-section__title">{{ club.title }}</h2>
    {%- if club.meets %}<p class="print-section__meta">Meets {{ club.meets }}</p>{%- endif %}
  </header>

  {%- assign thumb_src = club.thumbnail | default: site.club_thumbnail_default -%}
  {%- if thumb_src and thumb_src != "" %}
  <div class="print-thumbnail">
    <img src="{{ thumb_src | relative_url }}" alt="{{ club.title }} photo" class="print-thumbnail__img">
  </div>
  {%- endif %}

  {%- if club.advisors and club.advisors.size > 0 %}
  <section class="roster">
    <h3 class="roster__heading">
      {%- if club.advisors.size > 1 -%}{{ site.labels.advisors_many }}{%- else -%}{{ site.labels.advisors_one }}{%- endif -%}
    </h3>
    <div class="roster__grid roster__grid--lg">
      {%- for aid in club.advisors %}
        {% include person-card-print.html id=aid size="lg" %}
      {%- endfor %}
    </div>
  </section>
  {%- endif %}

  {%- if club.members and club.members.size > 0 %}
  <section class="roster">
    <h3 class="roster__heading">{{ site.labels.members }}</h3>
    <div class="roster__grid">
      {%- for mid in club.members %}
        {% include person-card-print.html id=mid %}
      {%- endfor %}
    </div>
  </section>
  {%- endif %}

  {%- if club.group_photos and club.group_photos.size > 0 %}
    {%- for gp in club.group_photos %}
    <section class="group-photo">
      <h3 class="group-photo__heading">Group Photo</h3>
      <figure class="group-photo__figure">
        <img src="{{ gp.src | relative_url }}" alt="{{ club.title }} group photo" class="group-photo__img">
        {%- if gp.annotation and gp.annotation.size > 0 %}
        <figcaption class="group-photo__caption">
          {%- if gp.caption %}<span class="group-photo__label">{{ gp.caption }}</span> {%- endif -%}
          {%- for pid in gp.annotation -%}
            {%- assign gpperson = site.data.people_by_id[pid] -%}
            {%- if gpperson -%}{{- gpperson.display_name -}}{%- unless forloop.last %}, {% endunless -%}{%- endif -%}
          {%- endfor %}
        </figcaption>
        {%- endif %}
      </figure>
    </section>
    {%- endfor %}
  {%- elsif club.group_photo %}
  <section class="group-photo">
    <h3 class="group-photo__heading">Group Photo</h3>
    <figure class="group-photo__figure">
      <img src="{{ club.group_photo | relative_url }}" alt="{{ club.title }} group photo" class="group-photo__img">
      {%- if club.photo_annotation and club.photo_annotation.size > 0 %}
      <figcaption class="group-photo__caption">
        {%- if club.photo_caption %}<span class="group-photo__label">{{ club.photo_caption }}</span> {%- endif -%}
        {%- for pid in club.photo_annotation -%}
          {%- assign gp2 = site.data.people_by_id[pid] -%}
          {%- if gp2 -%}{{- gp2.display_name -}}{%- unless forloop.last %}, {% endunless -%}{%- endif -%}
        {%- endfor %}
      </figcaption>
      {%- endif %}
    </figure>
  </section>
  {%- endif %}

</article>
{%- endfor %}

{%- comment -%} ═══ 5. SPORTS ═══ {%- endcomment -%}
{%- for team in site.sports %}
{%- assign team_slug = team.url | remove_first: '/sports/' | remove: '/' -%}
<article class="print-section print-page-break" id="print-section-sport-{{ team_slug }}">

  <header class="print-section__header">
    <p class="print-section__eyebrow">{{ site.labels.eyebrow_sport }}</p>
    <h2 class="print-section__title">{{ team.title }}</h2>
    {%- if team.season or team.record %}
      <p class="print-section__meta">
        {%- if team.season %}{{ team.season }}{% endif %}
        {%- if team.season and team.record %} · {% endif %}
        {%- if team.record %}Record: {{ team.record }}{% endif %}
      </p>
    {%- endif %}
  </header>

  {%- assign thumb_src = team.thumbnail | default: site.sport_thumbnail_default -%}
  {%- if thumb_src and thumb_src != "" %}
  <div class="print-thumbnail">
    <img src="{{ thumb_src | relative_url }}" alt="{{ team.title }} photo" class="print-thumbnail__img">
  </div>
  {%- endif %}

  {%- if team.coaches and team.coaches.size > 0 %}
  <section class="roster">
    <h3 class="roster__heading">
      {%- if team.coaches.size > 1 -%}{{ site.labels.coaches_many }}{%- else -%}{{ site.labels.coaches_one }}{%- endif -%}
    </h3>
    <div class="roster__grid roster__grid--lg">
      {%- for cid in team.coaches %}
        {% include person-card-print.html id=cid size="lg" %}
      {%- endfor %}
    </div>
  </section>
  {%- endif %}

  {%- if team.members and team.members.size > 0 %}
  <section class="roster">
    <h3 class="roster__heading">{{ site.labels.roster }}</h3>
    <div class="roster__grid">
      {%- for mid in team.members %}
        {% include person-card-print.html id=mid %}
      {%- endfor %}
    </div>
  </section>
  {%- endif %}

  {%- if team.group_photos and team.group_photos.size > 0 %}
    {%- for gp in team.group_photos %}
    <section class="group-photo">
      <h3 class="group-photo__heading">Group Photo</h3>
      <figure class="group-photo__figure">
        <img src="{{ gp.src | relative_url }}" alt="{{ team.title }} group photo" class="group-photo__img">
        {%- if gp.annotation and gp.annotation.size > 0 %}
        <figcaption class="group-photo__caption">
          {%- if gp.caption %}<span class="group-photo__label">{{ gp.caption }}</span> {%- endif -%}
          {%- for pid in gp.annotation -%}
            {%- assign gpperson = site.data.people_by_id[pid] -%}
            {%- if gpperson -%}{{- gpperson.display_name -}}{%- unless forloop.last %}, {% endunless -%}{%- endif -%}
          {%- endfor %}
        </figcaption>
        {%- endif %}
      </figure>
    </section>
    {%- endfor %}
  {%- elsif team.group_photo %}
  <section class="group-photo">
    <h3 class="group-photo__heading">Group Photo</h3>
    <figure class="group-photo__figure">
      <img src="{{ team.group_photo | relative_url }}" alt="{{ team.title }} group photo" class="group-photo__img">
      {%- if team.photo_annotation and team.photo_annotation.size > 0 %}
      <figcaption class="group-photo__caption">
        {%- if team.photo_caption %}<span class="group-photo__label">{{ team.photo_caption }}</span> {%- endif -%}
        {%- for pid in team.photo_annotation -%}
          {%- assign gp3 = site.data.people_by_id[pid] -%}
          {%- if gp3 -%}{{- gp3.display_name -}}{%- unless forloop.last %}, {% endunless -%}{%- endif -%}
        {%- endfor %}
      </figcaption>
      {%- endif %}
    </figure>
  </section>
  {%- endif %}

</article>
{%- endfor %}

{%- comment -%} ═══ 6. STAFF ═══ {%- endcomment -%}
{%- assign staff_only = site.data.people | where: "role", "staff" -%}
{%- assign teachers   = site.data.people | where: "role", "teacher" -%}
{%- assign all_staff  = staff_only | concat: teachers -%}
{%- if all_staff.size > 0 %}
<article class="print-section print-page-break" id="print-section-staff">
  <header class="print-section__header">
    <p class="print-section__eyebrow">{{ site.labels.eyebrow_staff }}</p>
    <h2 class="print-section__title">Faculty &amp; Staff</h2>
  </header>
  <section class="roster">
    <div class="roster__grid roster__grid--lg">
      {%- for person in all_staff %}
        {% include person-card-print.html id=person.id size="lg" %}
      {%- endfor %}
    </div>
  </section>
</article>
{%- endif %}

{%- comment -%} ═══ 7. PHOTO PAGES ═══ {%- endcomment -%}
{%- if site.photos and site.photos.size > 0 %}
{%- for pp in site.photos %}
{%- assign photo_slug = pp.url | remove_first: '/photos/' | remove: '/' -%}
<article class="print-section print-page-break" id="print-section-photo-{{ photo_slug }}">
  <header class="print-section__header">
    <p class="print-section__eyebrow">Photos</p>
    <h2 class="print-section__title">{{ pp.title }}</h2>
    {%- if pp.date %}<p class="print-section__meta">{{ pp.date }}</p>{%- endif %}
  </header>
  {%- include photo-gallery.html photos=pp.photos %}
</article>
{%- endfor %}
{%- endif %}

{%- comment -%} ═══ 8. SUPERLATIVES ═══ {%- endcomment -%}
{%- assign superlatives = site.data.superlatives -%}
{%- if superlatives and superlatives.size > 0 %}
<article class="print-section print-page-break" id="print-section-superlatives">
  <header class="print-section__header">
    <p class="print-section__eyebrow">{{ site.labels.eyebrow_superlatives | default: "Superlatives" }}</p>
    <h2 class="print-section__title">Class Superlatives</h2>
  </header>
  <div class="superlative-grid">
    {%- for s in superlatives %}
    {%- assign winner = site.data.people_by_id[s.winner] -%}
    {%- assign runner = site.data.people_by_id[s.runner_up] -%}
    <div class="superlative-card">
      <p class="superlative-card__category">{{ s.category }}</p>
      {%- if winner %}
      <div class="superlative-card__winner">
        <figure class="superlative-card__frame">
          <img
            src="{{ winner.photo | relative_url }}"
            alt="{{ winner.display_name }}"
            onerror="this.replaceWith(Object.assign(document.createElement('div'),{className:'superlative-card__fallback',textContent:{{ winner.initials | jsonify | escape }}}))">
        </figure>
        <span class="superlative-card__name">{{ winner.display_name }}</span>
        {%- if runner %}
        <span class="superlative-card__runner-up">Runner-up: {{ runner.display_name }}</span>
        {%- endif %}
      </div>
      {%- endif %}
    </div>
    {%- endfor %}
  </div>
</article>
{%- endif %}

{%- comment -%} ═══ 9. YEAR IN REVIEW ═══ {%- endcomment -%}
{%- assign yir = site.data.year_in_review -%}
{%- if yir and yir.sections and yir.sections.size > 0 %}
<article class="print-section print-page-break" id="print-section-yir">
  <header class="print-section__header">
    <p class="print-section__eyebrow">{{ site.labels.eyebrow_yir | default: "Year in Review" }}</p>
    <h2 class="print-section__title">{{ yir.school_year | default: "The Year" }} in Review</h2>
  </header>
  <div class="yir-grid">
    {%- for section in yir.sections %}
    <section class="yir-card">
      <h3 class="yir-card__title">
        {%- if section.icon %}<span class="yir-card__icon" aria-hidden="true">{{ section.icon }}</span>{%- endif -%}
        {{ section.title }}
      </h3>
      {%- if section.items and section.items.size > 0 %}
      <ul class="yir-card__list">
        {%- for item in section.items %}
        <li class="yir-card__item">{{ item }}</li>
        {%- endfor %}
      </ul>
      {%- endif %}
    </section>
    {%- endfor %}
  </div>
</article>
{%- endif %}

{%- comment -%} ═══ 10. STUDENT FAVORITES ═══ {%- endcomment -%}
{%- assign favorites = site.data.favorites -%}
{%- if favorites and favorites.size > 0 %}
<article class="print-section print-page-break" id="print-section-favorites">
  <header class="print-section__header">
    <p class="print-section__eyebrow">{{ site.labels.eyebrow_favorites | default: "Favorites" }}</p>
    <h2 class="print-section__title">Student Favorites</h2>
  </header>
  <div class="favorites-grid">
    {%- for fav in favorites %}
    {%- assign person = site.data.people_by_id[fav.id] -%}
    {%- if person %}
    <div class="favorites-card">
      <figure class="favorites-card__frame">
        <img
          src="{{ person.photo | relative_url }}"
          alt="{{ person.display_name }}"
          onerror="this.replaceWith(Object.assign(document.createElement('div'),{className:'favorites-card__fallback',textContent:{{ person.initials | jsonify | escape }}}))">
      </figure>
      <div class="favorites-card__body">
        <p class="favorites-card__name">{{ person.display_name }}</p>
        <dl class="favorites-card__list">
          {%- if fav.subject %}<dt>📚 Subject</dt><dd>{{ fav.subject }}</dd>{%- endif %}
          {%- if fav.book %}<dt>📖 Book</dt><dd>{{ fav.book }}</dd>{%- endif %}
          {%- if fav.lunch %}<dt>🍕 Lunch</dt><dd>{{ fav.lunch }}</dd>{%- endif %}
          {%- if fav.memory %}<dt>⭐ Memory</dt><dd>{{ fav.memory }}</dd>{%- endif %}
        </dl>
      </div>
    </div>
    {%- endif %}
    {%- endfor %}
  </div>
</article>
{%- endif %}

{%- comment -%} ═══ 11. DEDICATIONS & ADS ═══ {%- endcomment -%}
{%- assign dedications = site.data.dedications -%}
{%- if dedications and dedications.size > 0 %}
<article class="print-section print-page-break" id="print-section-dedications">
  <header class="print-section__header">
    <p class="print-section__eyebrow">{{ site.labels.eyebrow_dedications | default: "Dedications &amp; Ads" }}</p>
    <h2 class="print-section__title">Dedications &amp; Ads</h2>
  </header>
  <div class="dedications-grid">
    {%- for d in dedications %}
    {%- assign honoree = site.data.people_by_id[d.for] -%}
    <div class="dedication-card{% if d.size == 'half' %} dedication-card--half{% endif %}">
      {%- if honoree %}
      <div class="dedication-card__portrait">
        <figure class="dedication-card__frame">
          <img
            src="{{ honoree.photo | relative_url }}"
            alt="{{ honoree.display_name }}"
            onerror="this.replaceWith(Object.assign(document.createElement('div'),{className:'dedication-card__fallback',textContent:{{ honoree.initials | jsonify | escape }}}))">
        </figure>
        <span class="dedication-card__honoree-name">{{ honoree.display_name }}</span>
      </div>
      {%- endif %}
      <div class="dedication-card__content">
        <blockquote class="dedication-card__message">{{ d.message }}</blockquote>
        <p class="dedication-card__from">— {{ d.from }}</p>
      </div>
    </div>
    {%- endfor %}
  </div>
</article>
{%- endif %}

{%- comment -%} ═══ 12. AUTOGRAPHS ═══
  Number of autograph pages is controlled by `autograph_pages` in _config.yml.
  Update that value to change the count in both the print PDF and the web page.
{%- endcomment -%}
{%- assign autograph_count = site.autograph_pages | default: 2 -%}
{%- for autograph_n in (1..autograph_count) %}
<article class="print-section print-page-break">
  <header class="print-section__header">
    <p class="print-section__eyebrow">{{ site.labels.eyebrow_autographs | default: "Autographs" }}</p>
    <h2 class="print-section__title">Autographs</h2>
  </header>
  <div class="autograph-lines">
    {%- for _line in (1..18) %}
    <div class="autograph-line"></div>
    {%- endfor %}
  </div>
</article>
{%- endfor %}

{%- comment -%} ═══ 13. INDEX ═══ {%- endcomment -%}
{%- assign index_people = site.data.people | sort: "last" -%}
{%- if index_people and index_people.size > 0 %}
<article class="print-section print-page-break" id="print-section-index">
  <header class="print-section__header">
    <p class="print-section__eyebrow">Index</p>
    <h2 class="print-section__title">Index</h2>
  </header>
  <ul class="print-index">
    {%- for person in index_people %}
    {%- assign m = site.data.memberships[person.id] -%}
    <li class="print-index__entry">
      <span class="print-index__name">{{ person.last }}, {{ person.display_name }}</span>
      <span class="print-index__refs">
        {%- for group in m.staff -%}
          <a class="print-index__ref" href="#{{ group.print_id }}">Faculty &amp; Staff</a>
        {%- endfor -%}
        {%- for group in m.classes -%}
          <a class="print-index__ref" href="#{{ group.print_id }}">{{ group.title }}</a>
        {%- endfor -%}
        {%- for group in m.clubs -%}
          <a class="print-index__ref" href="#{{ group.print_id }}">{{ group.title }}</a>
        {%- endfor -%}
        {%- for group in m.sports -%}
          <a class="print-index__ref" href="#{{ group.print_id }}">{{ group.title }}</a>
        {%- endfor -%}
        {%- for group in m.photos -%}
          <a class="print-index__ref" href="#{{ group.print_id }}">{{ group.title }}</a>
        {%- endfor -%}
        {%- for group in m.superlatives -%}
          <a class="print-index__ref" href="#print-section-superlatives">{{ group.title }}</a>
        {%- endfor -%}
        {%- for group in m.dedications -%}
          <a class="print-index__ref" href="#print-section-dedications">Dedication</a>
        {%- endfor -%}
      </span>
    </li>
    {%- endfor %}
  </ul>
</article>
{%- endif %}

{%- comment -%} ═══ 14. BACK COVER ═══ {%- endcomment -%}
<section class="print-back-cover print-page-break">
  <div class="print-back-cover__accent-bar"></div>
  <div class="print-back-cover__body">
    <p class="print-back-cover__year">{{ site.school_year }}</p>
    <p class="print-back-cover__name">{{ site.title }}</p>
  </div>
  <div class="print-back-cover__accent-bar"></div>
</section>

{%- comment -%} ═══ 15. PRINT INSTRUCTIONS (screen only) ═══ {%- endcomment -%}
<section class="print-instructions no-print" id="print-instructions">
  <h2 class="print-instructions__heading">How to save and submit your yearbook to a book printing service</h2>

  <h3>Step 1 — Generate the PDF</h3>
  <ol>
    <li>Click the <strong>Print / Save as PDF</strong> button at the top of this page (or use your browser's print shortcut: <kbd>Ctrl+P</kbd> on Windows/Linux, <kbd>⌘P</kbd> on Mac).</li>
    <li>In the print dialog, set the <strong>Destination</strong> (or Printer) to <strong>"Save as PDF"</strong>.</li>
    <li>
      Apply these settings for book-quality output:
      <ul>
        <li><strong>Paper size:</strong> US Letter (8.5 × 11 in) — commonly used for yearbooks and accepted by most print services</li>
        <li><strong>Scale:</strong> 100% (do <em>not</em> check "Fit to page")</li>
        <li><strong>Margins:</strong> None (margins are already built into this page)</li>
        <li><strong>Background graphics:</strong> ✅ Enabled — required so background colors print</li>
        <li><strong>Headers and footers:</strong> Disabled (uncheck if your browser adds page numbers automatically)</li>
      </ul>
    </li>
    <li>Click <strong>Save</strong>. Your PDF will download.</li>
  </ol>
  <p><em>For the sharpest portraits, make sure your original photos are at least 300 dpi (pixels per inch). Print quality depends on the resolution of your source images — higher-resolution photos will reproduce much more clearly in the finished book.</em></p>

  <h3>Step 2 — Choose a book printing service</h3>
  <p>Several print-on-demand services accept uploaded PDFs with no minimum order:</p>
  <ul>
    <li>
      <strong><a href="https://www.lulu.com" target="_blank" rel="noopener noreferrer">Lulu.com</a></strong> —
      Free to set up. Upload a PDF, choose binding (perfect-bound or coil), and order as few or as many copies as you need.
      Accepts US Letter (8.5 × 11 in), RGB color PDF.
    </li>
    <li>
      <strong><a href="https://www.blurb.com" target="_blank" rel="noopener noreferrer">Blurb</a></strong> —
      Offers 8.5 × 11 in magazine and book formats. Upload via their PDF upload tool.
      Accepts RGB PDF; they recommend PDF/X-1a for color accuracy.
    </li>
    <li>
      <strong><a href="https://www.printingforless.com" target="_blank" rel="noopener noreferrer">Printing for Less</a></strong> —
      Professional print shop with volume pricing. Good for larger orders (20+ copies).
    </li>
  </ul>

  <h3>Step 3 — Submit to Lulu (example walkthrough)</h3>
  <ol>
    <li>Create a free account at <a href="https://www.lulu.com" target="_blank" rel="noopener noreferrer">lulu.com</a>.</li>
    <li>Click <strong>"Create" → "Print Book"</strong>.</li>
    <li>
      Choose your specifications:
      <ul>
        <li>Size: <strong>8.5 × 11 in</strong></li>
        <li>Binding: <strong>Perfect Bound</strong> (square spine, looks most like a real yearbook) or <strong>Coil Bound</strong> (lies flat when open)</li>
        <li>Paper: <strong>Standard Color</strong> (60 lb) or <strong>Premium Color</strong> (70 lb) for richer photos</li>
        <li>Cover: <strong>Matte</strong> or <strong>Glossy</strong> — glossy is traditional for yearbooks</li>
      </ul>
    </li>
    <li>Upload the PDF you generated in Step 1 as the interior file.</li>
    <li>Design or upload a cover image for the front and back cover (Lulu provides a cover creator tool).</li>
    <li>Preview, set your price (or order at cost for the school), and add to cart.</li>
    <li>Lulu prints and ships directly to you, typically within 5–10 business days.</li>
  </ol>

  <h3>Tips for the best results</h3>
  <ul>
    <li><strong>Page count:</strong> Most print services require an even number of pages. If your PDF has an odd number of pages, add a blank page at the end.</li>
    <li><strong>Bleed:</strong> This PDF uses a 0.75 in safe margin on all sides — well within the bleed requirements for standard print services.</li>
    <li><strong>Proof first:</strong> Order one copy to check color and quality before ordering in bulk.</li>
    <li><strong>Color mode:</strong> This PDF uses RGB color. Lulu and Blurb accept RGB; if your service requires CMYK, you can convert the PDF using Adobe Acrobat or a free tool such as <a href="https://www.ilovepdf.com" target="_blank" rel="noopener noreferrer">ilovepdf.com</a>.</li>
    <li><strong>Font embedding:</strong> When you print to PDF from Chrome or Firefox, all fonts are automatically embedded — no extra steps needed.</li>
  </ul>
</section>
