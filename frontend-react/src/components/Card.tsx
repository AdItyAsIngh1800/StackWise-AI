import { motion } from "framer-motion";

type Props = {
  children: React.ReactNode;
};

export default function Card({ children }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
      className="rounded-xl bg-white p-4 shadow transition hover:shadow-md dark:bg-gray-800"
    >
      {children}
    </motion.div>
  );
}