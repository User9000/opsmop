import os

class Page(object):

    def __init__(self, record, dest_dir):

        self.dest_path = os.path.join(dest_dir, "module_%s.rst" % record.name)
        self.elink = self.example_link(record.name)
        self.tlink = self.type_link(record.name)
        self.record = record

    def sphinx_link(self, link, title, prefix=""):
        return ":ref:`%s%s <%s>`_" % (prefix, title, link)

    def example_link(self, name):
        return "https://github.com/vespene-io/opsmop-demo/blob/master/module_docs/%s.py" % (name)

    def type_link(self, name):
        return "https://github.com/vespene-io/opsmop/tree/master/opsmop/types/%s.py" % (name)

    def provider_link(self, name):
        return "https://github.com/vespene-io/opsmop/tree/master/opsmop/providers/%s.py" % (name)

    def footer(self, name, top=False):
        buf = ""
        buf = buf + (name.title() + "\n")
        nlen = len(name)
        if not top:
            buf = buf + "-" * nlen
        else:
            buf = buf + "=" * nlen
        buf = buf + "\n"
        return buf


    def generate(self):

        record = self.record
        fd = open(self.dest_path, "w")

        # Slug and title
        fd.write(".. _module_%s:\n\n" % self.record.name)
        fd.write(self.footer(self.record.name.title() + " Module", top=True))

        # Description
        fd.write("\n")
        for line in record.description:
            fd.write("%s\n" % line)
        fd.write("\n")

        # Examples
        fd.write("\n")
        for e in record.examples:
            msg = "Example: %s" % e.name
            fd.write(self.footer(msg))
            fd.write("\n")
            for line in e.description:
                fd.write("%s\n" % line)
            fd.write("\n\ncode:")
            fd.write("\n")
            for line in e.code:
                fd.write("    %s\n" % line)
            fd.write("\n")

        # Links to Type Implementations on GitHub
        fd.write(self.footer("Type Implementations"))
        fd.write("* %s\n" % self.sphinx_link(self.type_link(record.name), record.name, prefix='opsmop.types.'))
        fd.write("\n")

        # Same for Providers
        fd.write(self.footer("Provider Implementations"))
        for p in record.providers:
            p1 = p.replace(".","/")
            fd.write("* %s\n" % self.sphinx_link(self.provider_link(p1), p, prefix='opsmop.providers.'))
        fd.write("\n")

        # if there are related modules, link to them all
        if len(record.related_modules):
            fd.write(self.footer("Related Modules"))
            for m in self.record.related_modules:
                fd.write("* :ref:`module_%s`\n" % m)
            fd.write("\n")

        # Link to other language chapters
        fd.write(self.footer("See Also"))
        fd.write("* :ref:`language`\n")
        fd.write("* :ref:`advanced`\n")
        fd.write("* :ref:`development`\n")
        fd.write("\n")

        # Done!
        fd.close()
        print("written: %s" % self.dest_path)