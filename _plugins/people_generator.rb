# =============================================================================
#  _plugins/people_generator.rb
# =============================================================================
#  This Jekyll plugin does two things at build time:
#
#  1. Creates an individual profile page at /people/<id>/ for every person
#     listed in _data/people.yml. You never have to write these pages by hand.
#
#  2. Builds a reverse index — for each person, the set of classes, clubs,
#     and sports they appear on. The person.html layout uses this to render
#     the "Appears in" section, so a student's profile always links back to
#     every roster that includes them, with zero manual work.
#
#  HOW IT RUNS:
#    GitHub Pages's native build doesn't allow custom plugins. That's why
#    this repo builds via GitHub Actions (see .github/workflows/build.yml)
#    instead — custom plugins like this one run fine there.
#
#  EDITING THIS FILE:
#    Most volunteers will never need to touch this. If you want to add more
#    derived fields to each person (e.g., a formatted grade label), add them
#    in `build_display_name` / `build_initials` style helpers below and
#    assign them to `p['your_field']` in `generate`. The fields will then be
#    available in the person.html layout as `{{ page.person.your_field }}`.
# =============================================================================

module Yearbook
  # ---------------------------------------------------------------------------
  # PersonPage — a lightweight Jekyll page object, one per person.
  # Points at _layouts/person.html and passes along the person record + their
  # memberships for the template to render.
  # ---------------------------------------------------------------------------
  class PersonPage < Jekyll::Page
    def initialize(site, base, person, memberships)
      @site = site
      @base = base
      @dir  = File.join('people', person['id'])  # → /people/<id>/index.html
      @name = 'index.html'

      self.process(@name)
      # Load the person layout file so Jekyll knows which template to render.
      self.read_yaml(File.join(base, '_layouts'), 'person.html') rescue nil
      self.data ||= {}
      self.data['layout']      = 'person'
      self.data['person']      = person        # → `page.person` in the layout
      self.data['memberships'] = memberships   # → `page.memberships`
      self.data['title']       = person['display_name']
      self.data['slug']        = person['id']
    end
  end

  # ---------------------------------------------------------------------------
  # PeopleGenerator — runs once per build. Normalizes every entry in people.yml,
  # then scans class/club/sport rosters to build the memberships index.
  # ---------------------------------------------------------------------------
  class PeopleGenerator < Jekyll::Generator
    safe true
    priority :high  # run before other generators, so downstream code sees data

    def generate(site)
      people = site.data['people'] || []
      default_path = site.config['photo_path_default'] || '/assets/images/people/{id}.jpg'

      # --- Step 1: Normalize each person record in place ------------------
      # Adds derived fields (display name, initials, photo URL, profile URL)
      # that the layouts depend on. Done once here so Liquid stays simple.
      by_id = {}
      people.each do |p|
        p['role']         ||= 'student'
        p['display_name']   = build_display_name(p)
        p['initials']       = build_initials(p)
        p['photo']        ||= default_path.gsub('{id}', p['id'])
        p['url']            = "/people/#{p['id']}/"
        by_id[p['id']]      = p
      end
      # Expose the by-ID lookup table for use in Liquid
      # (person-card.html uses `site.data.people_by_id[include.id]`).
      site.data['people_by_id'] = by_id

      # --- Step 2: Build reverse index of memberships ---------------------
      # For each person, collect every class/club/sport/photo-page that references them.
      # Structure: { "malcolm-wilkerson" => { classes: [...], clubs: [...], sports: [...], photos: [...] } }
      memberships = Hash.new { |h, k| h[k] = { 'classes' => [], 'clubs' => [], 'sports' => [], 'photos' => [] } }

      index_collection(site, 'classes', %w[students teachers], memberships)
      index_collection(site, 'clubs',   %w[members advisors],  memberships)
      index_collection(site, 'sports',  %w[members coaches],   memberships)
      index_photos(site, memberships)

      site.data['memberships'] = memberships

      # --- Step 3: Generate one profile page per person --------------------
      people.each do |person|
        site.pages << PersonPage.new(site, site.source, person, memberships[person['id']])
      end

      # --- Step 4: Add grade_sort to class documents ----------------------
      # Maps grade values to integers for correct ordering:
      #   PK → -2, K → -1, 1 → 1, 2 → 2, … so PK and K sort first.
      # Classes with no grade field default to 0 (between K and 1st grade).
      (site.collections['classes']&.docs || []).each do |doc|
        grade = doc.data['grade']
        doc.data['grade_sort'] = case grade.to_s.upcase
          when 'PK' then -2
          when 'K'  then -1
          when ''   then 0   # grade not set — place after K, before 1st
          else grade.to_i
        end
      end
    end

    private

    # Prefer nickname over first name for display (e.g. "Frankie" vs "Francis").
    def build_display_name(p)
      first = p['nickname'] && !p['nickname'].empty? ? p['nickname'] : p['first']
      "#{first} #{p['last']}".strip
    end

    # Two-letter fallback shown when a photo file is missing (e.g. "MW").
    def build_initials(p)
      "#{(p['first'] || '')[0]}#{(p['last'] || '')[0]}".upcase
    end

    # For a given collection, walk every doc and record membership in each
    # listed ID field. `id_fields` is e.g. %w[students teachers].
    def index_collection(site, coll_name, id_fields, memberships)
      (site.collections[coll_name]&.docs || []).each do |doc|
        id_fields.each do |field|
          (doc.data[field] || []).each do |pid|
            bucket = memberships[pid][coll_name]
            bucket << { 'title' => doc.data['title'], 'url' => doc.url, 'role' => field }
          end
        end
      end
    end

    # Walk every photo page and record each person who is labeled in at least
    # one photo on that page. Each photo page appears at most once per person,
    # even if the same person is labeled in multiple photos on the same page.
    def index_photos(site, memberships)
      (site.collections['photos']&.docs || []).each do |doc|
        title = doc.data['title']
        url   = doc.url
        # Collect unique person IDs labeled anywhere on this photo page.
        person_ids = (doc.data['photos'] || []).flat_map { |photo| photo['labels'] || [] }.uniq
        person_ids.each do |pid|
          memberships[pid]['photos'] << { 'title' => title, 'url' => url }
        end
      end
    end
  end
end
